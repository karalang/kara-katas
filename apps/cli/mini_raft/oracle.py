"""The oracle for mini_raft: the same simulator, written plainly in Python.

It follows the README's rules for the protocol (Raft's Figure 2), the
clock, the network and the random streams, so the Kāra port's event log
must match it line for line.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os

MASK = 0xFFFFFFFF
ELECTION_MIN = 150
ELECTION_SPREAD = 150
HEARTBEAT = 50
LAT_MIN = 2
LAT_SPREAD = 8


class Fail(Exception):
    pass


class Rng:
    """xorshift32."""

    def __init__(self, seed):
        self.x = seed & MASK or 1

    def next(self):
        x = self.x
        x ^= (x << 13) & MASK
        x ^= x >> 17
        x ^= (x << 5) & MASK
        self.x = x
        return x

    def below(self, n):
        return self.next() % n


class Node:
    def __init__(self, nid, seed):
        self.id = nid
        self.rng = Rng(seed * 1000 + nid * 7919)
        self.term = 0
        self.voted = 0
        self.log = []  # (term, command, client)
        self.alive = True
        self.reset_volatile()

    def reset_volatile(self):
        self.state = "follower"
        self.commit = 0
        self.applied = 0
        self.kv = {}
        self.votes = set()
        self.next_index = {}
        self.match_index = {}
        self.leader = 0
        self.deadline = 0
        self.beat = 0

    def last_index(self):
        return len(self.log)

    def last_term(self):
        return self.log[-1][0] if self.log else 0


class Sim:
    def __init__(self, n, seed, until):
        self.n = n
        self.seed = seed
        self.until = until
        self.nodes = {i: Node(i, seed) for i in range(1, n + 1)}
        self.net = Rng(seed * 31 + 17)
        self.queue = []  # (time, seq, src, dst, msg)
        self.seq = 0
        self.drop = 0
        self.groups = None
        self.now = 0
        self.out = []
        self.leaders = {}  # term -> leader id
        self.clients = []  # [name, command, status]
        self.reported = set()
        for nd in self.nodes.values():
            self.reset_timer(nd)

    def say(self, text):
        self.out.append(f"t={self.now} {text}")

    def majority(self):
        return self.n // 2 + 1

    def reset_timer(self, nd):
        nd.deadline = self.now + ELECTION_MIN + nd.rng.below(ELECTION_SPREAD)

    # -------------------------------------------------------- network

    def send(self, src, dst, msg):
        if self.drop > 0 and self.net.below(1000) < self.drop:
            return
        t = self.now + LAT_MIN + self.net.below(LAT_SPREAD)
        self.seq += 1
        self.queue.append((t, self.seq, src, dst, msg))

    def connected(self, a, b):
        if self.groups is None:
            return True
        return (a in self.groups[0]) == (b in self.groups[0])

    # -------------------------------------------------------- roles

    def become_follower(self, nd, term, why):
        was = nd.state
        if term > nd.term:
            nd.term = term
            nd.voted = 0
        nd.state = "follower"
        if was == "leader":
            # A leader's election timer has not run; start it afresh.
            self.reset_timer(nd)
        if was != "follower":
            self.say(f"n{nd.id} steps down to follower in term {nd.term} ({why})")

    def start_election(self, nd):
        nd.state = "candidate"
        nd.term += 1
        nd.voted = nd.id
        nd.votes = {nd.id}
        nd.leader = 0
        self.reset_timer(nd)
        self.say(f"n{nd.id} starts an election for term {nd.term}")
        for p in range(1, self.n + 1):
            if p != nd.id:
                self.send(nd.id, p, ("vote", nd.term, nd.last_index(), nd.last_term()))
        self.check_votes(nd)

    def check_votes(self, nd):
        if nd.state == "candidate" and len(nd.votes) >= self.majority():
            nd.state = "leader"
            nd.leader = nd.id
            voters = " ".join(f"n{v}" for v in sorted(nd.votes))
            self.say(f"n{nd.id} becomes leader of term {nd.term} (votes {voters})")
            if nd.term in self.leaders and self.leaders[nd.term] != nd.id:
                self.say(f"SAFETY: two leaders in term {nd.term}")
            self.leaders[nd.term] = nd.id
            nd.log.append((nd.term, "noop", ""))
            for p in range(1, self.n + 1):
                nd.next_index[p] = nd.last_index()
                nd.match_index[p] = 0
            nd.match_index[nd.id] = nd.last_index()
            self.broadcast(nd)

    def broadcast(self, nd):
        nd.beat = self.now + HEARTBEAT
        for p in range(1, self.n + 1):
            if p != nd.id:
                self.send_append(nd, p)

    def send_append(self, nd, p):
        prev = nd.next_index[p] - 1
        prev_term = nd.log[prev - 1][0] if prev > 0 else 0
        entries = nd.log[prev:prev + 4]
        self.send(nd.id, p, ("append", nd.term, prev, prev_term, list(entries), nd.commit))

    # -------------------------------------------------------- messages

    def deliver(self, src, nd, msg):
        kind, term = msg[0], msg[1]
        if term > nd.term:
            self.become_follower(nd, term, f"n{src} has term {term}")
            nd.leader = 0
        if kind == "vote":
            _, _, last_idx, last_term = msg
            up_to_date = (last_term, last_idx) >= (nd.last_term(), nd.last_index())
            grant = term == nd.term and nd.voted in (0, src) and up_to_date
            if grant:
                nd.voted = src
                self.reset_timer(nd)
            self.send(nd.id, src, ("voted", nd.term, grant))
        elif kind == "voted":
            granted = msg[2]
            if nd.state == "candidate" and term == nd.term and granted:
                nd.votes.add(src)
                self.check_votes(nd)
        elif kind == "append":
            _, _, prev, prev_term, entries, leader_commit = msg
            if term < nd.term:
                self.send(nd.id, src, ("appended", nd.term, False, 0))
                return
            if nd.state != "follower":
                self.become_follower(nd, term, f"n{src} leads term {term}")
            if nd.leader != src:
                nd.leader = src
            self.reset_timer(nd)
            if prev > nd.last_index() or (prev > 0 and nd.log[prev - 1][0] != prev_term):
                self.send(nd.id, src, ("appended", nd.term, False, 0))
                return
            i = prev
            for e in entries:
                if i < nd.last_index():
                    if nd.log[i][0] != e[0]:
                        dropped = nd.last_index() - i
                        del nd.log[i:]
                        self.say(f"n{nd.id} drops {dropped} conflicting entries from index {i + 1}")
                        nd.log.append(e)
                else:
                    nd.log.append(e)
                i += 1
            if leader_commit > nd.commit:
                nd.commit = min(leader_commit, prev + len(entries))
                self.apply(nd)
            self.send(nd.id, src, ("appended", nd.term, True, prev + len(entries)))
        elif kind == "appended":
            _, _, ok, match = msg
            if nd.state != "leader" or term != nd.term:
                return
            if ok:
                if match > nd.match_index[src]:
                    nd.match_index[src] = match
                nd.next_index[src] = nd.match_index[src] + 1
                self.advance_commit(nd)
                if nd.next_index[src] <= nd.last_index():
                    self.send_append(nd, src)
            else:
                nd.next_index[src] = max(1, nd.next_index[src] - 1)
                self.send_append(nd, src)

    def advance_commit(self, nd):
        for idx in range(nd.last_index(), nd.commit, -1):
            if nd.log[idx - 1][0] != nd.term:
                break
            have = sum(1 for p in range(1, self.n + 1) if nd.match_index[p] >= idx)
            if have >= self.majority():
                nd.commit = idx
                self.apply(nd)
                break

    def apply(self, nd):
        while nd.applied < nd.commit:
            nd.applied += 1
            term, cmd, client = nd.log[nd.applied - 1]
            f = cmd.split(" ")
            if f[0] == "set":
                nd.kv[f[1]] = f[2]
            elif f[0] == "del":
                nd.kv.pop(f[1], None)
            elif f[0] == "incr":
                old = nd.kv.get(f[1], "0")
                nd.kv[f[1]] = str((int(old) if old.isdigit() else 0) + int(f[2]))
            if nd.state == "leader" and client and client not in self.reported:
                self.reported.add(client)
                self.say(f"{client} committed: {cmd} at index {nd.applied} (term {term})")
                for c in self.clients:
                    if c[0] == client:
                        c[2] = f"committed at index {nd.applied}"

    # -------------------------------------------------------- the clock

    def tick(self):
        due = sorted(m for m in self.queue if m[0] == self.now)
        self.queue = [m for m in self.queue if m[0] != self.now]
        for _, _, src, dst, msg in due:
            nd = self.nodes[dst]
            if nd.alive and self.connected(src, dst):
                self.deliver(src, nd, msg)
        for i in range(1, self.n + 1):
            nd = self.nodes[i]
            if not nd.alive:
                continue
            if nd.state == "leader":
                if self.now >= nd.beat:
                    self.broadcast(nd)
            elif self.now >= nd.deadline:
                self.start_election(nd)

    # -------------------------------------------------------- targets

    def leader_node(self, among=None):
        best = None
        for i in range(1, self.n + 1):
            nd = self.nodes[i]
            if among is not None and i not in among:
                continue
            if nd.alive and nd.state == "leader" and (best is None or nd.term > best.term):
                best = nd
        return best

    def resolve(self, target):
        """A node for a client, crash or partition target, or None."""
        if target.startswith("n") and target[1:].isdigit():
            return self.nodes[int(target[1:])]
        if target == "leader":
            return self.leader_node()
        if target == "follower":
            for i in range(1, self.n + 1):
                nd = self.nodes[i]
                if nd.alive and nd.state != "leader":
                    return nd
            return None
        if target in ("minority", "majority"):
            if self.groups is None:
                return None
            a, b = self.groups
            small, big = (a, b) if len(a) < len(b) else (b, a)
            g = small if target == "minority" else big
            ld = self.leader_node(g)
            if ld:
                return ld
            for i in sorted(g):
                if self.nodes[i].alive:
                    return self.nodes[i]
        return None

    # -------------------------------------------------------- actions

    def act(self, words):
        cmd = words[0]
        if cmd == "client":
            target, op = words[1], " ".join(words[2:])
            name = f"c{len(self.clients) + 1}"
            self.clients.append([name, op, "not committed"])
            nd = self.resolve(target)
            if nd is None:
                self.say(f"{name} {op}: no {target} to send to")
                self.clients[-1][2] = "never sent"
                return
            # A client follows one redirect, as client libraries do.
            for attempt in range(2):
                if not nd.alive:
                    self.say(f"{name} -> n{nd.id}: no answer (down)")
                    return
                if nd.state == "leader":
                    break
                if nd.leader == 0 or attempt == 1:
                    hint = f"try n{nd.leader}" if nd.leader else "no leader known"
                    self.say(f"{name} -> n{nd.id}: not the leader, {hint}")
                    return
                self.say(f"{name} -> n{nd.id}: not the leader, redirected to n{nd.leader}")
                nd = self.nodes[nd.leader]
            nd.log.append((nd.term, op, name))
            nd.match_index[nd.id] = nd.last_index()
            self.say(f"{name} -> n{nd.id}: {op} appended at index {nd.last_index()} (term {nd.term})")
            self.broadcast(nd)
        elif cmd == "crash":
            nd = self.resolve(words[1])
            if nd is None or not nd.alive:
                self.say(f"crash {words[1]}: nothing to crash")
                return
            nd.alive = False
            self.say(f"n{nd.id} crashes ({nd.state}, term {nd.term})")
        elif cmd == "restart":
            if words[1] == "all":
                todo = [self.nodes[i] for i in range(1, self.n + 1) if not self.nodes[i].alive]
            else:
                nd = self.resolve(words[1])
                todo = [nd] if nd is not None and not nd.alive else []
            if not todo:
                self.say(f"restart {words[1]}: nothing is down")
            for nd in todo:
                nd.alive = True
                nd.reset_volatile()
                self.reset_timer(nd)
                self.say(f"n{nd.id} restarts (term {nd.term}, log {nd.last_index()})")
        elif cmd == "partition":
            spec = words[1]
            if spec == "leader+1":
                ld = self.leader_node()
                if ld is None:
                    self.say("partition leader+1: no leader")
                    return
                other = next(i for i in range(1, self.n + 1) if i != ld.id and self.nodes[i].alive)
                side = {ld.id, other}
            elif spec == "follower":
                nd = self.resolve("follower")
                if nd is None:
                    self.say("partition follower: no follower")
                    return
                side = {nd.id}
            else:
                side = {int(x) for x in spec.split(",")}
            rest = set(range(1, self.n + 1)) - side
            self.groups = (side, rest)
            self.say("partition " + " | ".join(
                " ".join(f"n{i}" for i in sorted(g)) for g in (side, rest)))
        elif cmd == "heal":
            self.groups = None
            self.say("heal")
        elif cmd == "drop":
            self.drop = int(words[1])
            self.say(f"drop {self.drop} per mille")
        elif cmd == "status":
            self.say("status")
            self.out.extend(self.status_lines())

    def status_lines(self):
        lines = []
        for i in range(1, self.n + 1):
            nd = self.nodes[i]
            state = nd.state if nd.alive else "down"
            kv = ", ".join(f"{k}={v}" for k, v in sorted(nd.kv.items()))
            lines.append(f"  n{i}: {state:<9} term {nd.term}, log {nd.last_index()} "
                         f"(last term {nd.last_term()}), commit {nd.commit}, kv {{{kv}}}")
        return lines

    # -------------------------------------------------------- checks

    def safety(self):
        out = []
        logs = [self.nodes[i].log for i in range(1, self.n + 1)]
        bad = []
        for a in range(self.n):
            for b in range(a + 1, self.n):
                la, lb = logs[a], logs[b]
                for idx in range(min(len(la), len(lb)) - 1, -1, -1):
                    if la[idx][0] == lb[idx][0]:
                        if la[:idx + 1] != lb[:idx + 1]:
                            bad.append(f"n{a + 1}/n{b + 1} at {idx + 1}")
                        break
        out.append("log matching " + ("ok" if not bad else "FAILED: " + ", ".join(bad)))
        commits = [(self.nodes[i].commit, i) for i in range(1, self.n + 1)]
        hi, who = max(commits)
        ref = self.nodes[who].log[:hi]
        bad = [f"n{i}" for c, i in commits if self.nodes[i].log[:c] != ref[:c]]
        out.append("committed prefixes " + ("ok" if not bad else "FAILED: " + ", ".join(bad)))
        return out


def parse(name, text):
    n, seed, until = 0, 0, 0
    acts = []
    errs = []
    for no, line in enumerate(text.split("\n"), 1):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        w = t.split()
        try:
            if w[0] in ("nodes", "seed", "until"):
                if len(w) != 2 or not w[1].isdigit():
                    raise Fail(f"{w[0]} needs a number")
                v = int(w[1])
                if w[0] == "nodes":
                    if not 1 <= v <= 9:
                        raise Fail("nodes must be 1 to 9")
                    n = v
                elif w[0] == "seed":
                    seed = v
                else:
                    until = v
                continue
            if not w[0].isdigit():
                raise Fail(f"unknown line: {t}")
            at = int(w[0])
            if acts and at < acts[-1][0]:
                raise Fail(f"time {at} is before the line above")
            if len(w) < 2:
                raise Fail("missing action")
            a = w[1]
            args = w[2:]
            if a == "client":
                if len(args) < 2:
                    raise Fail("client needs a target and a command")
                op = args[1:]
                ok = ((op[0] == "set" and len(op) == 3)
                      or (op[0] == "del" and len(op) == 2)
                      or (op[0] == "incr" and len(op) == 3 and op[2].isdigit()))
                if not ok:
                    raise Fail(f"bad command: {' '.join(op)}")
            elif a in ("crash", "restart", "partition", "drop"):
                if len(args) != 1:
                    raise Fail(f"{a} needs one argument")
                if a == "drop" and not (args[0].isdigit() and int(args[0]) <= 1000):
                    raise Fail("drop needs 0 to 1000")
                if a == "partition" and args[0] not in ("leader+1", "follower"):
                    parts = args[0].split(",")
                    if not all(p.isdigit() and 1 <= int(p) <= max(n, 1) for p in parts):
                        raise Fail("partition needs leader+1, follower or node numbers")
            elif a in ("heal", "status"):
                if args:
                    raise Fail(f"{a} takes no arguments")
            else:
                raise Fail(f"unknown action: {a}")
            if a in ("client", "crash", "restart") and args[0].startswith("n") \
                    and args[0][1:].isdigit() and not 1 <= int(args[0][1:]) <= max(n, 1):
                raise Fail(f"no node {args[0]}")
            acts.append((at, w[1:]))
        except Fail as e:
            errs.append(f"{name} line {no}: {e}")
    if n == 0:
        errs.append(f"{name}: no nodes line")
    return n, seed, until, acts, errs


def run(name, text):
    n, seed, until, acts, errs = parse(name, text)
    out = [f"== {name}: {n} nodes, seed {seed}, until t={until}"]
    if errs:
        out += ["! " + e for e in errs]
        return out
    sim = Sim(n, seed, until)
    k = 0
    for t in range(0, until + 1):
        sim.now = t
        while k < len(acts) and acts[k][0] == t:
            sim.act(acts[k][1])
            k += 1
        sim.tick()
    sim.out.append(f"-- end at t={until}")
    sim.out.extend(sim.status_lines())
    terms = sorted(sim.leaders.items())
    sim.out.append("  leaders: " + (" ".join(f"{t}:n{i}" for t, i in terms) or "none"))
    done = [c for c in sim.clients if c[2].startswith("committed")]
    rest = [c for c in sim.clients if not c[2].startswith("committed")]
    line = f"  clients: {len(done)} of {len(sim.clients)} committed"
    if rest:
        line += "; " + ", ".join(f"{c[0]} {c[2]}" for c in rest)
    sim.out.append(line)
    sim.out += ["  " + s for s in sim.safety()]
    return out + sim.out


def main():
    names = sorted(x for x in os.listdir("data") if x.endswith(".sim"))
    out = []
    for name in names:
        with open(os.path.join("data", name), encoding="utf-8") as fh:
            out += run(name, fh.read())
    print("\n".join(out))


main()
