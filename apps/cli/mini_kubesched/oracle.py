"""The oracle for mini_kubesched: the same scheduler written plainly in
Python from the rules in README.md. Prints what the program prints, and
writes data/out/bindings.txt.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os

MILLI_DEFAULT = 100            # the CPU a pod with no request is scored at
MEM_DEFAULT = 200 * 1024 * 1024
EFFECTS = ("NoSchedule", "PreferNoSchedule", "NoExecute")
OPS = ("In", "NotIn", "Exists", "DoesNotExist", "Gt", "Lt")
MEM_UNITS = [("Ki", 1024), ("Mi", 1024 ** 2), ("Gi", 1024 ** 3), ("Ti", 1024 ** 4),
             ("k", 1000), ("M", 1000 ** 2), ("G", 1000 ** 3), ("T", 1000 ** 4)]


class Bad(Exception):
    pass


def digits(s):
    return s != "" and all("0" <= c <= "9" for c in s)


def parse_int(s):
    """An optional '-' and digits; None otherwise."""
    body = s[1:] if s.startswith("-") else s
    if not digits(body) or len(body) > 15:
        return None
    return -int(body) if s.startswith("-") else int(body)


def parse_cpu(s):
    if s.endswith("m"):
        if not digits(s[:-1]) or len(s) > 13:
            raise Bad(f"bad quantity '{s}'")
        return int(s[:-1])
    whole, dot, frac = s.partition(".")
    if not digits(whole) or len(whole) > 9 or (dot and (not digits(frac) or len(frac) > 3)):
        raise Bad(f"bad quantity '{s}'")
    return int(whole) * 1000 + (int(frac.ljust(3, "0")) if dot else 0)


def parse_mem(s):
    for suf, mul in MEM_UNITS:
        if s.endswith(suf):
            n = s[:-len(suf)]
            if not digits(n) or len(n) > 9:
                raise Bad(f"bad quantity '{s}'")
            return int(n) * mul
    if not digits(s) or len(s) > 15:
        raise Bad(f"bad quantity '{s}'")
    return int(s)


def show_cpu(m):
    return f"{m}m"


def show_mem(b):
    for suf, mul in (("Gi", 1024 ** 3), ("Mi", 1024 ** 2), ("Ki", 1024)):
        if b != 0 and b % mul == 0:
            return f"{b // mul}{suf}"
    return str(b)


def parse_label(tok):
    k, eq, v = tok.partition("=")
    if not eq or k == "":
        raise Bad(f"bad label '{tok}'")
    return k, v


def parse_selector(tok):
    return [parse_label(t) for t in tok.split(",")]


def parse_taint(tok):
    kv, colon, eff = tok.rpartition(":")
    if not colon or kv == "":
        raise Bad(f"bad taint '{tok}'")
    if eff not in EFFECTS:
        raise Bad(f"bad effect '{eff}'")
    k, eq, v = kv.partition("=")
    if k == "":
        raise Bad(f"bad taint '{tok}'")
    return (k, v, eff)


def parse_toleration(tok):
    """(key, op, value, effect); key '' with Exists tolerates everything."""
    if tok == "*":
        return ("", "Exists", "", "")
    kv, eff = tok, ""
    if ":" in tok:
        kv, _, eff = tok.rpartition(":")
        if eff not in EFFECTS:
            raise Bad(f"bad effect '{eff}'")
    k, eq, v = kv.partition("=")
    if k == "":
        raise Bad(f"bad toleration '{tok}'")
    return (k, "Equal" if eq else "Exists", v, eff)


def parse_requirement(toks):
    text = " ".join(toks)
    if len(toks) < 2 or toks[1] not in OPS:
        if len(toks) >= 2:
            raise Bad(f"bad operator '{toks[1]}'")
        raise Bad(f"bad requirement '{text}'")
    key, op = toks[0], toks[1]
    if op in ("Exists", "DoesNotExist"):
        if len(toks) != 2:
            raise Bad(f"bad requirement '{text}'")
        return (key, op, [])
    if len(toks) != 3:
        raise Bad(f"bad requirement '{text}'")
    vals = toks[2].split(",")
    if op in ("Gt", "Lt") and (len(vals) != 1 or parse_int(vals[0]) is None):
        raise Bad(f"bad requirement '{text}'")
    return (key, op, vals)


def requirement_holds(req, labels):
    key, op, vals = req
    has = key in labels
    if op == "In":
        return has and labels[key] in vals
    if op == "NotIn":
        return not has or labels[key] not in vals
    if op == "Exists":
        return has
    if op == "DoesNotExist":
        return not has
    if not has:
        return False
    n = parse_int(labels[key])
    if n is None:
        return False
    return n > parse_int(vals[0]) if op == "Gt" else n < parse_int(vals[0])


class Node:
    def __init__(self, name, cpu, mem, pods, where):
        self.name, self.cpu, self.mem, self.max_pods = name, cpu, mem, pods
        self.labels = {"hostname": name}
        self.taints = []
        self.cordoned = False
        self.where = where


class Pod:
    def __init__(self, name, prio, where):
        self.name, self.prio, self.where = name, prio, where
        self.ns = name.split("/")[0]
        self.cpu = 0
        self.mem = 0
        self.labels = {}
        self.select = []
        self.require = []
        self.prefer = []
        self.tolerations = []
        self.apart = []
        self.spread = []
        self.node = None
        self.seq = 0


def parse_header(toks, where):
    kind = toks[0]
    if kind == "node":
        if len(toks) < 2:
            raise Bad("node needs a name")
        name = toks[1]
        got = {}
        for t in toks[2:]:
            k, eq, v = t.partition("=")
            if not eq or k not in ("cpu", "memory", "pods"):
                raise Bad(f"unknown field '{t}'")
            if k == "cpu":
                got[k] = parse_cpu(v)
            elif k == "memory":
                got[k] = parse_mem(v)
            else:
                n = parse_int(v)
                if n is None or n < 0:
                    raise Bad(f"bad quantity '{v}'")
                got[k] = n
        if len(got) != 3:
            raise Bad(f"node '{name}' needs cpu, memory and pods")
        return Node(name, got["cpu"], got["memory"], got["pods"], where)
    if kind == "pod":
        if len(toks) < 2:
            raise Bad("pod needs a name")
        name = toks[1]
        ns, slash, short = name.partition("/")
        if not slash or ns == "" or short == "":
            raise Bad(f"pod name '{name}' needs a namespace")
        prio = 0
        for t in toks[2:]:
            k, eq, v = t.partition("=")
            if not eq or k != "priority":
                raise Bad(f"unknown field '{t}'")
            n = parse_int(v)
            if n is None:
                raise Bad(f"bad priority '{v}'")
            prio = n
        return Pod(name, prio, where)
    raise Bad(f"unknown directive '{kind}'")


def parse_field(obj, toks):
    f, rest = toks[0], toks[1:]
    if isinstance(obj, Node):
        if f == "label":
            for t in rest:
                k, v = parse_label(t)
                obj.labels[k] = v
        elif f == "taint":
            for t in rest:
                obj.taints.append(parse_taint(t))
        elif f == "unschedulable" and not rest:
            obj.cordoned = True
        else:
            raise Bad(f"unknown field '{f}'")
        return
    if f == "request":
        for t in rest:
            k, eq, v = t.partition("=")
            if k == "cpu" and eq:
                obj.cpu = parse_cpu(v)
            elif k == "memory" and eq:
                obj.mem = parse_mem(v)
            else:
                raise Bad(f"unknown field '{t}'")
    elif f == "label":
        for t in rest:
            k, v = parse_label(t)
            obj.labels[k] = v
    elif f == "select":
        for t in rest:
            obj.select.append(parse_label(t))
    elif f == "require":
        obj.require.append(parse_requirement(rest))
    elif f == "prefer":
        w = parse_int(rest[0]) if rest else None
        if w is None or w < 1 or w > 100:
            raise Bad(f"bad weight '{rest[0] if rest else ''}'")
        obj.prefer.append((w, parse_requirement(rest[1:])))
    elif f == "tolerate":
        for t in rest:
            obj.tolerations.append(parse_toleration(t))
    elif f == "apart":
        if len(rest) != 2:
            raise Bad(f"bad term '{' '.join(rest)}'")
        obj.apart.append((rest[0], parse_selector(rest[1])))
    elif f == "spread":
        if len(rest) != 3:
            raise Bad(f"bad term '{' '.join(rest)}'")
        skew = parse_int(rest[1])
        if skew is None or skew < 1:
            raise Bad(f"bad skew '{rest[1]}'")
        obj.spread.append((rest[0], skew, parse_selector(rest[2])))
    else:
        raise Bad(f"unknown field '{f}'")


def parse_file(path, text):
    """(nodes, pods, errors) in line order."""
    nodes, pods, errors = [], [], []
    cur = None
    bad = False

    def close():
        if cur is not None and not bad:
            (nodes if isinstance(cur, Node) else pods).append(cur)

    for i, raw in enumerate(text.split("\n")):
        line = raw.partition("#")[0]
        toks = line.split()
        if not toks:
            continue
        where = f"{path}:{i + 1}"
        if line[0] in " \t":
            if cur is None:
                if not bad:
                    errors.append(f"{where}: field outside a block")
                continue
            if bad:
                continue
            try:
                parse_field(cur, toks)
            except Bad as e:
                errors.append(f"{where}: {e}")
                bad = True
            continue
        close()
        cur, bad = None, False
        try:
            cur = parse_header(toks, where)
        except Bad as e:
            errors.append(f"{where}: {e}")
            bad = True
    close()
    return nodes, pods, errors


# ------------------------------------------------------------ the cluster

def selector_matches(sel, ns, pod):
    return pod.ns == ns and all(pod.labels.get(k) == v for k, v in sel)


def tolerates(tols, taint):
    k, v, eff = taint
    for tk, op, tv, te in tols:
        if te != "" and te != eff:
            continue
        if op == "Exists" and (tk == "" or tk == k):
            return True
        if op == "Equal" and tk == k and tv == v:
            return True
    return False


def show_taint(t):
    k, v, eff = t
    return f"{k}={v}:{eff}" if v else f"{k}:{eff}"


class Cluster:
    def __init__(self, out):
        self.nodes = {}
        self.pods = {}
        self.pending = []
        self.next_seq = 0
        self.out = out

    def admit(self, nodes, pods):
        for n in nodes:
            if n.name in self.nodes:
                self.out.append(f"{n.where}: duplicate node '{n.name}'")
                continue
            self.nodes[n.name] = n
        for p in pods:
            if p.name in self.pods:
                self.out.append(f"{p.where}: duplicate pod '{p.name}'")
                continue
            p.seq = self.next_seq
            self.next_seq += 1
            self.pods[p.name] = p
            self.pending.append(p.name)

    def node_names(self):
        return sorted(self.nodes)

    def on(self, node):
        return [p for p in self.pods.values() if p.node == node]

    def used(self, node, skip=()):
        c = m = k = 0
        for p in self.pods.values():
            if p.node == node and p.name not in skip:
                c += p.cpu
                m += p.mem
                k += 1
        return c, m, k

    def affinity_ok(self, pod, n):
        if any(n.labels.get(k) != v for k, v in pod.select):
            return False
        return all(requirement_holds(r, n.labels) for r in pod.require)

    def filter(self, pod, n, skip=()):
        """The reasons node n refuses pod, [] when it fits; pods named in
        skip are treated as gone."""
        if n.cordoned:
            return ["node(s) were unschedulable"]
        for t in n.taints:
            if t[2] != "PreferNoSchedule" and not tolerates(pod.tolerations, t):
                return [f"node(s) had untolerated taint {{{t[0]}: {t[1]}}}"]
        if not self.affinity_ok(pod, n):
            return ["node(s) didn't match Pod's node affinity/selector"]
        c, m, k = self.used(n.name, skip)
        why = []
        if k + 1 > n.max_pods:
            why.append("Too many pods")
        if c + pod.cpu > n.cpu:
            why.append("Insufficient cpu")
        if m + pod.mem > n.mem:
            why.append("Insufficient memory")
        if why:
            return why
        for key, skew, sel in pod.spread:
            if key not in n.labels:
                return ["node(s) didn't match pod topology spread constraints"]
            counts, eligible = {}, set()
            for m2 in self.nodes.values():
                if key in m2.labels and self.affinity_ok(pod, m2):
                    counts.setdefault(m2.labels[key], 0)
                    eligible.add(m2.name)
            for p in self.pods.values():
                if p.node not in eligible or p.name in skip or p.name == pod.name:
                    continue
                if selector_matches(sel, pod.ns, p):
                    counts[self.nodes[p.node].labels[key]] += 1
            me = 1 if selector_matches(sel, pod.ns, pod) else 0
            if counts[n.labels[key]] + me - min(counts.values()) > skew:
                return ["node(s) didn't match pod topology spread constraints"]
        for key, sel in pod.apart:
            if key not in n.labels:
                continue
            for p in self.pods.values():
                if p.node is None or p.name in skip or p.name == pod.name:
                    continue
                m2 = self.nodes[p.node]
                if m2.labels.get(key) == n.labels[key] and selector_matches(sel, pod.ns, p):
                    return ["node(s) didn't match pod anti-affinity rules"]
        for p in self.pods.values():
            if p.node is None or p.name in skip or p.name == pod.name:
                continue
            m2 = self.nodes[p.node]
            for key, sel in p.apart:
                if key in n.labels and m2.labels.get(key) == n.labels[key] \
                        and selector_matches(sel, p.ns, pod):
                    return ["node(s) didn't satisfy existing pods anti-affinity rules"]
        return []

    def scores(self, pod, feasible):
        """Total score per feasible node name."""
        least, bal, aff, taint, spread = {}, {}, {}, {}, {}
        pc = pod.cpu or MILLI_DEFAULT
        pm = pod.mem or MEM_DEFAULT
        for n in feasible:
            c = m = 0
            for p in self.on(n.name):
                c += p.cpu or MILLI_DEFAULT
                m += p.mem or MEM_DEFAULT
            c += pc
            m += pm
            lc = max(n.cpu - c, 0) * 100 // n.cpu if n.cpu else 0
            lm = max(n.mem - m, 0) * 100 // n.mem if n.mem else 0
            least[n.name] = (lc + lm) // 2
            fc = min(c * 10000 // n.cpu, 10000) if n.cpu else 10000
            fm = min(m * 10000 // n.mem, 10000) if n.mem else 10000
            bal[n.name] = (20000 - abs(fc - fm)) // 200
            aff[n.name] = sum(w for w, r in pod.prefer if requirement_holds(r, n.labels))
            taint[n.name] = sum(1 for t in n.taints
                                if t[2] == "PreferNoSchedule" and not tolerates(pod.tolerations, t))
            s = 0
            for key, skew, sel in pod.spread:
                for p in self.pods.values():
                    if p.node is None or p.name == pod.name:
                        continue
                    if self.nodes[p.node].labels.get(key) == n.labels[key] \
                            and selector_matches(sel, pod.ns, p):
                        s += 1
            spread[n.name] = s
        hi = max(aff.values())
        for k in aff:
            aff[k] = aff[k] * 100 // hi if hi else 0
        hi = max(taint.values())
        for k in taint:
            taint[k] = 100 - taint[k] * 100 // hi if hi else 100
        if pod.spread:
            hi, lo = max(spread.values()), min(spread.values())
            for k in spread:
                spread[k] = (hi + lo - spread[k]) * 100 // hi if hi else 100
        else:
            for k in spread:
                spread[k] = 0
        return {k: least[k] + bal[k] + 2 * aff[k] + 3 * taint[k] + 2 * spread[k] for k in least}

    def preempt(self, pod):
        """(node, victims) for the best node to preempt on, or None."""
        best = None
        for name in self.node_names():
            n = self.nodes[name]
            why = self.filter(pod, n)
            if not all(w in ("Too many pods", "Insufficient cpu", "Insufficient memory") for w in why):
                continue
            lower = [p for p in self.on(name) if p.prio < pod.prio]
            if not lower:
                continue
            gone = {p.name for p in lower}
            if self.filter(pod, n, gone):
                continue
            lower.sort(key=lambda p: (-p.prio, p.seq))
            for p in lower:
                gone.discard(p.name)
                if self.filter(pod, n, gone):
                    gone.add(p.name)
            victims = sorted(gone)
            prios = [self.pods[v].prio for v in victims]
            key = (max(prios), sum(prios), len(victims), name)
            if best is None or key < best[0]:
                best = (key, name, victims)
        return None if best is None else (best[1], best[2])

    def schedule(self):
        queue = sorted(self.pending, key=lambda q: (-self.pods[q].prio, self.pods[q].seq))
        self.pending = []
        bound = 0
        for name in queue:
            pod = self.pods[name]
            feasible, reasons = [], {}
            for nn in self.node_names():
                why = self.filter(pod, self.nodes[nn])
                if why:
                    for w in why:
                        reasons[w] = reasons.get(w, 0) + 1
                else:
                    feasible.append(self.nodes[nn])
            if feasible:
                sc = self.scores(pod, feasible)
                top = max(sc.values())
                pick = min(k for k in sc if sc[k] == top)
                pod.node = pick
                bound += 1
                self.out.append(f"bind {name} -> {pick} (score {top})")
                continue
            got = self.preempt(pod)
            if got is not None:
                node, victims = got
                self.out.append(f"preempt on {node} for {name}: evicts {', '.join(victims)}")
                for v in victims:
                    self.pods[v].node = None
                    self.pending.append(v)
                pod.node = node
                bound += 1
                self.out.append(f"bind {name} -> {node} (after preemption)")
                continue
            parts = sorted(f"{c} {w}" for w, c in reasons.items())
            self.out.append(f"FailedScheduling {name}: 0/{len(self.nodes)} nodes are available: "
                            + ", ".join(parts) + ".")
            self.pending.append(name)
        self.out.append(f"bound {bound}, pending {len(self.pending)}")

    def evict(self, name, why):
        p = self.pods[name]
        self.out.append(f"evict {name} from {p.node} ({why})")
        p.node = None
        self.pending.append(name)

    def event(self, toks):
        cmd, args = toks[0], toks[1:]
        if cmd == "schedule" and not args:
            self.schedule()
        elif cmd == "apply" and len(args) == 1:
            try:
                text = read(args[0])
            except OSError:
                raise Bad(f"cannot read {args[0]}")
            ns, ps, errs = parse_file(args[0], text)
            self.out.append(f"{args[0]}: {len(ns)} nodes, {len(ps)} pods")
            self.out.extend(errs)
            self.admit(ns, ps)
        elif cmd == "delete" and len(args) == 1:
            p = self.pods.get(args[0])
            if p is None:
                raise Bad(f"no pod '{args[0]}'")
            del self.pods[args[0]]
            if args[0] in self.pending:
                self.pending.remove(args[0])
            self.out.append(f"deleted {args[0]}")
        elif cmd in ("cordon", "uncordon", "drain", "fail", "taint", "untaint") and args:
            n = self.nodes.get(args[0])
            if n is None:
                raise Bad(f"no node '{args[0]}'")
            if cmd == "cordon" and len(args) == 1:
                n.cordoned = True
                self.out.append(f"node {n.name} cordoned")
            elif cmd == "uncordon" and len(args) == 1:
                n.cordoned = False
                self.out.append(f"node {n.name} uncordoned")
            elif cmd == "drain" and len(args) == 1:
                n.cordoned = True
                for p in sorted(self.on(n.name), key=lambda p: p.name):
                    self.evict(p.name, "drain")
                self.out.append(f"node {n.name} drained")
            elif cmd == "fail" and len(args) == 1:
                gone = sorted(p.name for p in self.on(n.name))
                for q in gone:
                    self.pods[q].node = None
                    self.pending.append(q)
                del self.nodes[n.name]
                self.out.append(f"node {n.name} failed: {len(gone)} pods back to pending")
            elif cmd == "taint" and len(args) == 2:
                t = parse_taint(args[1])
                n.taints.append(t)
                self.out.append(f"node {n.name} tainted {show_taint(t)}")
                if t[2] == "NoExecute":
                    for p in sorted(self.on(n.name), key=lambda p: p.name):
                        if not tolerates(p.tolerations, t):
                            self.evict(p.name, f"taint {show_taint(t)}")
            elif cmd == "untaint" and len(args) == 2:
                before = len(n.taints)
                n.taints = [t for t in n.taints if t[0] != args[1]]
                self.out.append(f"node {n.name} untainted {args[1]} ({before - len(n.taints)} removed)")
            else:
                raise Bad(f"bad event '{' '.join(toks)}'")
        elif cmd == "show" and args == ["pods"]:
            rows = [["NAMESPACE", "NAME", "PRIORITY", "STATUS", "NODE"]]
            for name in sorted(self.pods):
                p = self.pods[name]
                rows.append([p.ns, name.split("/", 1)[1], str(p.prio),
                             "Running" if p.node else "Pending", p.node or "<none>"])
            table(rows, self.out)
        elif cmd == "show" and args == ["nodes"]:
            rows = [["NAME", "STATUS", "CPU", "MEMORY", "PODS", "TAINTS"]]
            for name in self.node_names():
                n = self.nodes[name]
                c, m, k = self.used(name)
                rows.append([name, "Ready,SchedulingDisabled" if n.cordoned else "Ready",
                             f"{show_cpu(c)}/{show_cpu(n.cpu)} ({c * 100 // n.cpu if n.cpu else 0}%)",
                             f"{show_mem(m)}/{show_mem(n.mem)} ({m * 100 // n.mem if n.mem else 0}%)",
                             f"{k}/{n.max_pods}",
                             ",".join(show_taint(t) for t in n.taints) or "<none>"])
            table(rows, self.out)
        elif cmd == "show" and args == ["pending"]:
            q = sorted(self.pending, key=lambda q: (-self.pods[q].prio, self.pods[q].seq))
            self.out.append(f"{len(q)} pending" + (": " + ", ".join(q) if q else ""))
        else:
            raise Bad(f"bad event '{' '.join(toks)}'")


def table(rows, out):
    w = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    for r in rows:
        out.append("   ".join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip())


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def main():
    names = sorted(n for n in os.listdir("data")
                   if n.endswith(".nodes") or n.endswith(".pods"))
    out = ["== load"]
    nodes, pods = [], []
    for name in names:
        path = f"data/{name}"
        ns, ps, errs = parse_file(path, read(path))
        out.append(f"{path}: {len(ns)} nodes, {len(ps)} pods")
        out.extend(errs)
        nodes.extend(ns)
        pods.extend(ps)
    c = Cluster(out)
    c.admit(nodes, pods)
    out.append(f"{len(c.nodes)} nodes, {len(c.pods)} pods")
    out.append("== events")
    for i, raw in enumerate(read("data/events.txt").split("\n")):
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        out.append(f"> {line}")
        try:
            c.event(line.split())
        except Bad as e:
            out.append(f"error: data/events.txt:{i + 1}: {e}")
    rows = sorted(f"{p.name} {p.node}" for p in c.pods.values() if p.node)
    body = "".join(r + "\n" for r in rows)
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/bindings.txt", "w", encoding="utf-8", newline="") as fh:
        fh.write(body)
    back = read("data/out/bindings.txt")
    lines = [ln for ln in back.split("\n") if ln]
    out.append("== write")
    out.append(f"data/out/bindings.txt: {len(lines)} bindings, {len(back.encode())} bytes")
    per = {}
    for ln in lines:
        node = ln.split(" ")[1]
        per[node] = per.get(node, 0) + 1
    out.append(", ".join(f"{k} {per[k]}" for k in sorted(per)))
    print("\n".join(out))


main()
