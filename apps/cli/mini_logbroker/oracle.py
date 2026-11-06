"""Reference implementation of mini_logbroker (README.md is the spec).

Run from this directory after mk.py: python3 -I -B oracle.py"""
import os
import re
import shutil
import zlib

NAME = re.compile(r"[a-z0-9_.-]{1,40}\Z")
DIGITS = re.compile(r"[0-9]{1,9}\Z")
DUR = re.compile(r"([0-9]{1,7})([smh]?)\Z")
TIME = re.compile(r"([0-9]{2}):([0-9]{2}):([0-9]{2})\Z")
ROOT = "data/out/logs"
OFFSETS = "__consumer_offsets"
NONE = -1


def fmt(t):
    return f"{t // 3600:02}:{t // 60 % 60:02}:{t % 60:02}"


def num(s, lo, hi):
    if not DIGITS.match(s):
        return None
    v = int(s)
    return v if lo <= v <= hi else None


def dur(s):
    m = DUR.match(s)
    if not m:
        return None
    return int(m.group(1)) * {"": 1, "s": 1, "m": 60, "h": 3600}[m.group(2)]


def show_dur(v):
    if v == NONE:
        return "none"
    if v % 3600 == 0 and v > 0:
        return f"{v // 3600}h"
    if v % 60 == 0 and v > 0:
        return f"{v // 60}m"
    return f"{v}s"


def murmur2(data):
    m = 0x5BD1E995
    h = (0x9747B28C ^ len(data)) & 0xFFFFFFFF
    n = len(data) // 4
    for i in range(n):
        k = data[4 * i] | data[4 * i + 1] << 8 | data[4 * i + 2] << 16 | data[4 * i + 3] << 24
        k = (k * m) & 0xFFFFFFFF
        k ^= k >> 24
        k = (k * m) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF
        h ^= k
    rest = len(data) % 4
    base = n * 4
    if rest == 3:
        h ^= data[base + 2] << 16
    if rest >= 2:
        h ^= data[base + 1] << 8
    if rest >= 1:
        h ^= data[base]
        h = (h * m) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * m) & 0xFFFFFFFF
    h ^= h >> 15
    return h & 0x7FFFFFFF


# ------------------------------------------------------------ topics.conf

class Topic:
    def __init__(self, name):
        self.name = name
        self.partitions = 0
        self.segment_bytes = 1024
        self.retention = NONE
        self.retention_bytes = NONE
        self.cleanup = "delete"
        self.delete_retention = 3600


def parse_topics(text):
    topics, errors = [], []
    for no, raw in enumerate(text.split("\n"), 1):
        line = raw.split("#", 1)[0]
        toks = line.split()
        if not toks:
            continue
        where = f"topics.conf:{no}: "
        if toks[0] != "topic":
            errors.append(where + f"expected 'topic', found '{toks[0]}'")
            continue
        if len(toks) < 2:
            errors.append(where + "topic needs a name")
            continue
        name = toks[1]
        if not NAME.match(name):
            errors.append(where + f"bad topic name '{name}'")
            continue
        if name.startswith("__"):
            errors.append(where + f"topic name '{name}' is reserved")
            continue
        if any(t.name == name for t in topics):
            errors.append(where + f"topic {name} already defined")
            continue
        t = Topic(name)
        seen = []
        err = None
        for tok in toks[2:]:
            if "=" not in tok:
                err = f"expected key=value, found '{tok}'"
                break
            k, v = tok.split("=", 1)
            if k in seen:
                err = f"duplicate setting {k}"
                break
            seen.append(k)
            bad = f"bad value for {k}: '{v}'"
            if k == "partitions":
                x = num(v, 1, 16)
                if x is None:
                    err = bad
                    break
                t.partitions = x
            elif k == "segment_bytes":
                x = num(v, 64, 1048576)
                if x is None:
                    err = bad
                    break
                t.segment_bytes = x
            elif k == "retention":
                x = NONE if v == "none" else dur(v)
                if x is None or x == 0:
                    err = bad
                    break
                t.retention = x
            elif k == "retention_bytes":
                x = NONE if v == "none" else num(v, 1, 1000000000)
                if x is None:
                    err = bad
                    break
                t.retention_bytes = x
            elif k == "cleanup":
                if v not in ("delete", "compact"):
                    err = bad
                    break
                t.cleanup = v
            elif k == "delete_retention":
                x = dur(v)
                if x is None:
                    err = bad
                    break
                t.delete_retention = x
            else:
                err = f"unknown setting {k}"
                break
        if err is None and t.partitions == 0:
            err = "partitions is required"
        if err is None and t.cleanup == "compact" and (t.retention != NONE or t.retention_bytes != NONE):
            err = "a compacted topic has no retention"
        if err is not None:
            errors.append(where + err)
            continue
        topics.append(t)
    return topics, errors


def internal_topic():
    t = Topic(OFFSETS)
    t.partitions = 3
    t.segment_bytes = 512
    t.cleanup = "compact"
    t.delete_retention = 0
    return t


# ------------------------------------------------------------ script.txt

def parse_script(text):
    evs = []
    for no, raw in enumerate(text.split("\n"), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        toks = line.split()
        m = TIME.match(toks[0])
        ev = {"no": no, "line": line, "at": 0, "toks": toks[1:], "err": ""}
        if not m or int(m.group(2)) > 59 or int(m.group(3)) > 59:
            ev["err"] = f"bad time '{toks[0]}'"
        else:
            ev["at"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            if len(toks) < 2:
                ev["err"] = "missing command"
        evs.append(ev)
    return evs


# ------------------------------------------------------------ records

def enc(b):
    return "-" if b is None else ":" + b.hex()


def record_line(off, ts, key, val):
    body = f"{off} {ts} k{enc(key)} v{enc(val)}"
    return f"{body} {zlib.crc32(body.encode()):08x}\n"


def dec(tok, tag):
    if tok == tag + "-":
        return True, None
    if not tok.startswith(tag + ":"):
        return False, None
    h = tok[2:]
    if len(h) % 2 or any(c not in "0123456789abcdef" for c in h):
        return False, None
    return True, bytes.fromhex(h)


def parse_record(line):
    """A line without its newline -> (offset, ts, key, val) or a reason."""
    f = line.split(" ")
    if len(f) != 5 or not DIGITS.match(f[0]) or not DIGITS.match(f[1]):
        return "bad record"
    ok1, key = dec(f[2], "k")
    ok2, val = dec(f[3], "v")
    if not ok1 or not ok2 or len(f[4]) != 8:
        return "bad record"
    body = " ".join(f[:4])
    if f"{zlib.crc32(body.encode()):08x}" != f[4]:
        return "bad checksum"
    return (int(f[0]), int(f[1]), key, val)


def show_key(k):
    return "-" if k is None else k.decode()


def show_val(v):
    return "null" if v is None else v.decode()


class Segment:
    def __init__(self, base):
        self.base = base
        self.recs = []   # (offset, ts, key, val)
        self.size = 0


class Part:
    def __init__(self, topic, p):
        self.topic = topic
        self.p = p
        self.segs = [Segment(0)]
        self.end = 0
        self.start = 0

    def name(self):
        return f"{self.topic.name}-{self.p}"

    def dir(self):
        return f"{ROOT}/{self.name()}"

    def path(self, seg):
        return f"{self.dir()}/{seg.base:020}.log"

    def write(self, seg):
        with open(self.path(seg), "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(record_line(*r) for r in seg.recs))


# ------------------------------------------------------------ broker

class Group:
    def __init__(self, name, reset):
        self.name = name
        self.reset = reset
        self.members = {}     # member -> list of topics
        self.generation = 0
        self.assign = {}      # member -> list of (topic, p)
        self.pos = {}         # (topic, p) -> position
        self.committed = {}   # (topic, p) -> offset


class Broker:
    def __init__(self, topics):
        self.topics = topics + [internal_topic()]
        self.parts = {}
        self.groups = {}
        self.rr = {}
        self.now = 0
        self.down = False
        self.out = []

    def topic(self, name):
        for t in self.topics:
            if t.name == name:
                return t
        return None

    def fresh(self):
        shutil.rmtree(ROOT, ignore_errors=True)
        for t in self.topics:
            for p in range(t.partitions):
                part = Part(t, p)
                os.makedirs(part.dir())
                part.write(part.segs[0])
                self.parts[(t.name, p)] = part

    # ---- append

    def append(self, part, key, val):
        t = part.topic
        line = record_line(part.end, self.now, key, val)
        act = part.segs[-1]
        if act.recs and act.size + len(line) > t.segment_bytes:
            act = Segment(part.end)
            part.segs.append(act)
            self.out.append(f"roll {part.name()} at {part.end}")
        act.recs.append((part.end, self.now, key, val))
        act.size += len(line)
        with open(part.path(act), "a", encoding="utf-8", newline="") as fh:
            fh.write(line)
        part.end += 1
        return part.end - 1

    def choose(self, t, key):
        if key is None:
            n = self.rr.get(t.name, 0)
            self.rr[t.name] = n + 1
            return n % t.partitions
        return murmur2(key) % t.partitions

    def target(self, spec):
        name, _, ps = spec.partition(":")
        t = self.topic(name)
        if t is None:
            raise ValueError(f"unknown topic {name}")
        if t.name == OFFSETS:
            raise ValueError(f"topic {OFFSETS} is internal")
        p = None
        if ps or spec.endswith(":"):
            p = num(ps, 0, 99)
            if p is None or p >= t.partitions:
                raise ValueError(f"partition {ps} out of range for {name}")
        return t, p

    def produce(self, toks):
        if len(toks) < 3:
            raise ValueError("usage: produce <topic>[:<p>] <key|-> <value...|null>")
        t, p = self.target(toks[0])
        key = None if toks[1] == "-" else toks[1].encode()
        rest = " ".join(toks[2:])
        val = None if rest == "null" else rest.encode()
        if t.cleanup == "compact" and key is None:
            raise ValueError(f"compacted topic {t.name} needs a key")
        if p is None:
            p = self.choose(t, key)
        off = self.append(self.parts[(t.name, p)], key, val)
        self.out.append(f"ok {t.name}-{p}@{off}")

    def batch(self, toks):
        if len(toks) != 4:
            raise ValueError("usage: batch <topic> <count> <keys> <prefix>")
        t, p = self.target(toks[0])
        if p is not None:
            raise ValueError("batch takes a topic, not a partition")
        count = num(toks[1], 1, 1000)
        keys = num(toks[2], 0, 1000)
        if count is None:
            raise ValueError(f"bad count '{toks[1]}'")
        if keys is None:
            raise ValueError(f"bad key count '{toks[2]}'")
        if t.cleanup == "compact" and keys == 0:
            raise ValueError(f"compacted topic {t.name} needs a key")
        got = {}
        for i in range(count):
            key = None if keys == 0 else f"k{i % keys}".encode()
            q = self.choose(t, key)
            off = self.append(self.parts[(t.name, q)], key, f"{toks[3]}{i}".encode())
            lo, _ = got.get(q, (off, off))
            got[q] = (lo, off)
        shown = " ".join(f"{t.name}-{q}={got[q][0]}..{got[q][1]}" for q in sorted(got))
        self.out.append(f"ok {count} records: {shown}")

    # ---- fetch

    def read(self, part, off, mx):
        recs = []
        for seg in part.segs:
            for r in seg.recs:
                if r[0] >= off and len(recs) < mx:
                    recs.append(r)
        return recs

    def fetch(self, toks):
        if len(toks) not in (2, 3):
            raise ValueError("usage: fetch <topic>:<p> <offset> [max]")
        t, p = self.target(toks[0])
        if p is None:
            raise ValueError("fetch needs a partition")
        part = self.parts[(t.name, p)]
        off = num(toks[1], 0, 999999999)
        if off is None:
            raise ValueError(f"bad offset '{toks[1]}'")
        mx = 10
        if len(toks) == 3:
            mx = num(toks[2], 1, 1000)
            if mx is None:
                raise ValueError(f"bad max '{toks[2]}'")
        if off < part.start or off > part.end:
            raise ValueError(f"offset {off} out of range [{part.start}, {part.end}]")
        recs = self.read(part, off, mx)
        nxt = recs[-1][0] + 1 if recs else off
        self.out.append(f"{part.name()} @{off}: {len(recs)} records, next {nxt}")
        for r in recs:
            self.out.append(f"  {r[0]} {show_key(r[2])} {show_val(r[3])}")

    # ---- groups

    def offsets_part(self, group):
        return self.parts[(OFFSETS, murmur2(group.encode()) % 3)]

    def write_offset(self, group, key, val):
        self.append(self.offsets_part(group), key.encode(), None if val is None else val.encode())

    def rebalance(self, g):
        g.generation += 1
        g.pos = {}
        g.assign = {m: [] for m in g.members}
        names = sorted({t for ts in g.members.values() for t in ts})
        for name in names:
            subs = sorted(m for m, ts in g.members.items() if name in ts)
            n = self.topic(name).partitions
            per, extra = divmod(n, len(subs))
            at = 0
            for i, m in enumerate(subs):
                k = per + (1 if i < extra else 0)
                g.assign[m] += [(name, q) for q in range(at, at + k)]
                at += k
        if not g.members:
            self.out.append(f"group {g.name} generation {g.generation}: empty")
            return
        shown = " ".join(
            m + "=[" + ",".join(f"{a}-{b}" for a, b in g.assign[m]) + "]" for m in sorted(g.members))
        self.out.append(f"group {g.name} generation {g.generation}: {shown}")

    def join(self, toks):
        if len(toks) not in (3, 4):
            raise ValueError("usage: join <group> <member> <topic,...> [reset=earliest|latest]")
        gname, member = toks[0], toks[1]
        for what, v in (("group", gname), ("member", member)):
            if not NAME.match(v):
                raise ValueError(f"bad {what} name '{v}'")
        subs = []
        for name in toks[2].split(","):
            t = self.topic(name)
            if t is None:
                raise ValueError(f"unknown topic {name}")
            if t.name == OFFSETS:
                raise ValueError(f"topic {OFFSETS} is internal")
            if name in subs:
                raise ValueError(f"topic {name} listed twice")
            subs.append(name)
        reset = "earliest"
        if len(toks) == 4:
            if toks[3] not in ("reset=earliest", "reset=latest"):
                raise ValueError(f"bad option '{toks[3]}'")
            reset = toks[3][6:]
        g = self.groups.get(gname)
        if g is None:
            g = Group(gname, reset)
            self.groups[gname] = g
            self.write_offset(gname, f"group/{gname}", reset)
        elif len(toks) == 4 and g.reset != reset:
            raise ValueError(f"group {gname} resets to {g.reset}")
        if member in g.members:
            raise ValueError(f"member {member} already in group {gname}")
        g.members[member] = subs
        self.rebalance(g)

    def member(self, gname, member):
        g = self.groups.get(gname)
        if g is None:
            raise ValueError(f"unknown group {gname}")
        if member not in g.members:
            raise ValueError(f"member {member} is not in group {gname}")
        return g

    def leave(self, toks):
        if len(toks) != 2:
            raise ValueError("usage: leave <group> <member>")
        g = self.member(toks[0], toks[1])
        del g.members[toks[1]]
        self.rebalance(g)

    def poll(self, toks):
        if len(toks) not in (2, 3):
            raise ValueError("usage: poll <group> <member> [max]")
        g = self.member(toks[0], toks[1])
        mx = 5
        if len(toks) == 3:
            mx = num(toks[2], 1, 1000)
            if mx is None:
                raise ValueError(f"bad max '{toks[2]}'")
        lines = []
        got = 0
        for tp in g.assign[toks[1]]:
            part = self.parts[tp]
            name = part.name()
            if tp not in g.pos:
                if tp in g.committed:
                    g.pos[tp] = g.committed[tp]
                else:
                    g.pos[tp] = part.start if g.reset == "earliest" else part.end
            pos = g.pos[tp]
            if pos < part.start or pos > part.end:
                to = part.start if g.reset == "earliest" else part.end
                lines.append(f"  reset {name} from {pos} to {to} (out of range)")
                g.pos[tp] = pos = to
            if got >= mx:
                continue
            recs = self.read(part, pos, mx - got)
            for r in recs:
                lines.append(f"  {name} {r[0]} {show_key(r[2])} {show_val(r[3])}")
            if recs:
                g.pos[tp] = recs[-1][0] + 1
            got += len(recs)
        self.out.append(f"poll {g.name}/{toks[1]}: {got} records")
        self.out.extend(lines)

    def commit(self, toks):
        if len(toks) != 2:
            raise ValueError("usage: commit <group> <member>")
        g = self.member(toks[0], toks[1])
        done = []
        for tp in g.assign[toks[1]]:
            if tp in g.pos:
                self.write_offset(g.name, f"offset/{g.name}/{tp[0]}/{tp[1]}", str(g.pos[tp]))
                g.committed[tp] = g.pos[tp]
                done.append(f"{tp[0]}-{tp[1]}={g.pos[tp]}")
        if done:
            self.out.append(f"commit {g.name}/{toks[1]}: " + " ".join(done))
        else:
            self.out.append(f"commit {g.name}/{toks[1]}: nothing to commit")

    def lag(self, toks):
        if len(toks) != 1:
            raise ValueError("usage: lag <group>")
        g = self.groups.get(toks[0])
        if g is None:
            raise ValueError(f"unknown group {toks[0]}")
        if not g.committed:
            self.out.append(f"lag {g.name}: no committed offsets")
            return
        total = 0
        lines = []
        for tp in sorted(g.committed):
            part = self.parts[tp]
            c = g.committed[tp]
            total += part.end - c
            lines.append(f"  {part.name()} committed={c} end={part.end} lag={part.end - c}")
        self.out.append(f"lag {g.name}: {total}")
        self.out.extend(lines)

    def delete_group(self, toks):
        if len(toks) != 1:
            raise ValueError("usage: delete-group <group>")
        g = self.groups.get(toks[0])
        if g is None:
            raise ValueError(f"unknown group {toks[0]}")
        if g.members:
            raise ValueError(f"group {g.name} has members")
        for tp in sorted(g.committed):
            self.write_offset(g.name, f"offset/{g.name}/{tp[0]}/{tp[1]}", None)
        self.write_offset(g.name, f"group/{g.name}", None)
        self.out.append(f"deleted group {g.name}: {len(g.committed)} offsets")
        del self.groups[g.name]

    # ---- cleaning

    def ordered_parts(self, policy):
        for t in sorted(self.topics, key=lambda t: t.name):
            if t.cleanup == policy:
                for p in range(t.partitions):
                    yield self.parts[(t.name, p)]

    def retention(self, toks):
        if toks:
            raise ValueError("usage: retention")
        any_ = False
        for part in self.ordered_parts("delete"):
            t = part.topic
            gone = []
            total = sum(s.size for s in part.segs)
            while len(part.segs) > 1:
                seg = part.segs[0]
                old = t.retention != NONE and seg.recs[-1][1] <= self.now - t.retention
                big = t.retention_bytes != NONE and total - seg.size >= t.retention_bytes
                if not (old or big):
                    break
                part.segs.pop(0)
                total -= seg.size
                os.remove(part.path(seg))
                gone.append(seg.base)
            if gone:
                any_ = True
                part.start = part.segs[0].base
                shown = ", ".join(str(b) for b in gone)
                self.out.append(f"retention {part.name()}: deleted segments [{shown}], log start {part.start}")
        if not any_:
            self.out.append("retention: nothing to delete")

    def compact(self, toks):
        if toks:
            raise ValueError("usage: compact")
        any_ = False
        for part in self.ordered_parts("compact"):
            t = part.topic
            latest = {}
            for seg in part.segs:
                for r in seg.recs:
                    latest[r[2]] = r[0]
            kept = total = tombs = 0
            changed = False
            for seg in part.segs[:-1]:
                keep = []
                for r in seg.recs:
                    total += 1
                    if latest[r[2]] != r[0]:
                        continue
                    if r[3] is None and r[1] <= self.now - t.delete_retention:
                        tombs += 1
                        continue
                    keep.append(r)
                kept += len(keep)
                if len(keep) != len(seg.recs):
                    changed = True
                    seg.recs = keep
                    seg.size = sum(len(record_line(*r)) for r in keep)
            if not changed:
                continue
            any_ = True
            live = [part.segs[0]]
            for seg in part.segs[1:-1]:
                if seg.recs:
                    live.append(seg)
                else:
                    os.remove(part.path(seg))
            live.append(part.segs[-1])
            for seg in live[:-1]:
                part.write(seg)
            part.segs = live
            shown = ", ".join(str(s.base) for s in live)
            self.out.append(
                f"compact {part.name()}: kept {kept} of {total} records, removed {tombs} tombstones, "
                f"segments [{shown}]")
        if not any_:
            self.out.append("compact: nothing to clean")

    # ---- describe

    def describe_topic(self, t):
        ret = f", retention {show_dur(t.retention)}" if t.retention != NONE else ""
        rb = f", retention_bytes {t.retention_bytes}" if t.retention_bytes != NONE else ""
        self.out.append(
            f"topic {t.name}: partitions {t.partitions}, cleanup {t.cleanup}, "
            f"segment_bytes {t.segment_bytes}{ret}{rb}")
        for p in range(t.partitions):
            part = self.parts[(t.name, p)]
            segs = ", ".join(f"{s.base}:{s.size}" for s in part.segs)
            self.out.append(f"  {part.name()} start={part.start} end={part.end} segments=[{segs}]")

    def describe(self, toks):
        if len(toks) != 1:
            raise ValueError("usage: describe <topic>")
        t = self.topic(toks[0])
        if t is None:
            raise ValueError(f"unknown topic {toks[0]}")
        self.describe_topic(t)

    # ---- crash and recovery

    def crash(self, toks):
        if len(toks) > 1:
            raise ValueError("usage: crash [<topic>:<p>:<bytes>]")
        torn = None
        if toks:
            f = toks[0].split(":")
            if len(f) != 3:
                raise ValueError(f"bad tear '{toks[0]}'")
            t = self.topic(f[0])
            if t is None:
                raise ValueError(f"unknown topic {f[0]}")
            p = num(f[1], 0, 99)
            if p is None or p >= t.partitions:
                raise ValueError(f"partition {f[1]} out of range for {f[0]}")
            part = self.parts[(t.name, p)]
            act = part.segs[-1]
            n = num(f[2], 1, 1000000)
            if n is None or n > act.size:
                raise ValueError(f"cannot tear {f[2]} bytes from a {act.size}-byte segment")
            torn = (part, act, n)
        self.out.append("broker crashed")
        if torn:
            part, act, n = torn
            with open(part.path(act), "rb") as fh:
                data = fh.read()
            with open(part.path(act), "wb") as fh:
                fh.write(data[:len(data) - n])
            self.out.append(f"tore {n} bytes off {part.name()} segment {act.base}")
        self.down = True
        self.parts = {}
        self.groups = {}
        self.rr = {}

    def load(self, report):
        """Reads every partition back from disk. Returns (parts, records)."""
        parts = {}
        count = 0
        for t in self.topics:
            for p in range(t.partitions):
                part = Part(t, p)
                names = sorted(n for n in os.listdir(part.dir()) if n.endswith(".log"))
                segs = []
                prev = -1
                bad = None
                for n in names:
                    seg = Segment(int(n[:-4]))
                    if bad is not None:
                        os.remove(f"{part.dir()}/{n}")
                        continue
                    with open(f"{part.dir()}/{n}", "rb") as fh:
                        data = fh.read().decode("utf-8")
                    pos = 0
                    while pos < len(data):
                        nl = data.find("\n", pos)
                        rec = "torn record" if nl < 0 else parse_record(data[pos:nl])
                        if not isinstance(rec, str) and (rec[0] <= prev or rec[0] < seg.base):
                            rec = "offset out of order"
                        if isinstance(rec, str):
                            bad = (rec, prev + 1)
                            with open(f"{part.dir()}/{n}", "wb") as fh:
                                fh.write(data[:pos].encode())
                            break
                        seg.recs.append(rec)
                        seg.size += nl + 1 - pos
                        prev = rec[0]
                        pos = nl + 1
                    segs.append(seg)
                part.segs = segs
                part.start = segs[0].base
                part.end = max(prev + 1, segs[-1].base)
                if bad is not None and report:
                    self.out.append(f"truncated {part.name()} at offset {bad[1]}: {bad[0]}")
                count += sum(len(s.recs) for s in segs)
                parts[(t.name, p)] = part
        return parts, count

    def restart(self, toks):
        if toks:
            raise ValueError("usage: restart")
        self.parts, count = self.load(True)
        self.down = False
        self.out.append(f"recovered {len(self.parts)} partitions, {count} records")
        state = {}
        for p in range(3):
            for seg in self.parts[(OFFSETS, p)].segs:
                for r in seg.recs:
                    state[r[2].decode()] = None if r[3] is None else r[3].decode()
        for k in sorted(state):
            v = state[k]
            if v is None:
                continue
            f = k.split("/")
            if f[0] == "group":
                self.groups[f[1]] = Group(f[1], v)
        for k in sorted(state):
            v = state[k]
            f = k.split("/")
            if v is not None and f[0] == "offset" and f[1] in self.groups:
                self.groups[f[1]].committed[(f[2], int(f[3]))] = int(v)
        if self.groups:
            shown = ", ".join(f"{g} ({len(self.groups[g].committed)} offsets)" for g in sorted(self.groups))
            self.out.append(f"groups: {shown}")
        else:
            self.out.append("groups: none")

    # ---- dispatch

    def command(self, toks):
        cmd, args = toks[0], toks[1:]
        if self.down and cmd != "restart":
            raise ValueError("broker is down")
        table = {
            "produce": self.produce, "batch": self.batch, "fetch": self.fetch,
            "join": self.join, "leave": self.leave, "poll": self.poll, "commit": self.commit,
            "lag": self.lag, "delete-group": self.delete_group, "retention": self.retention,
            "compact": self.compact, "describe": self.describe, "crash": self.crash,
            "restart": self.restart,
        }
        if cmd not in table:
            raise ValueError(f"unknown command '{cmd}'")
        if cmd == "restart" and not self.down:
            raise ValueError("broker is running")
        table[cmd](args)


def main():
    with open("data/topics.conf", encoding="utf-8") as fh:
        topics, errors = parse_topics(fh.read())
    with open("data/script.txt", encoding="utf-8") as fh:
        evs = parse_script(fh.read())
    b = Broker(topics)
    b.out.append("== load")
    b.out.append(f"topics.conf: {len(topics)} topics")
    b.out.extend(errors)
    b.out.append(f"script.txt: {len(evs)} events")
    b.fresh()
    b.out.append("== events")
    for ev in evs:
        err = ev["err"]
        if not err and ev["at"] < b.now:
            err = "time goes back"
        b.out.append(f"> {ev['line']}")
        if not err:
            b.now = ev["at"]
            try:
                b.command(ev["toks"])
            except ValueError as e:
                err = str(e)
        if err:
            b.out.append(f"error: script.txt:{ev['no']}: {err}")
    b.out.append(f"== end {fmt(b.now)}")
    if b.down:
        b.out.append("broker is down")
    else:
        for t in b.topics:
            b.describe_topic(t)
        for name in sorted(b.groups):
            g = b.groups[name]
            ms = ",".join(sorted(g.members)) or "-"
            b.out.append(f"group {name}: reset {g.reset}, generation {g.generation}, members {ms}, "
                         f"{len(g.committed)} committed offsets")
        disk, count = b.load(False)
        same = all(
            [r for s in disk[k].segs for r in s.recs] == [r for s in b.parts[k].segs for r in s.recs]
            and disk[k].start == b.parts[k].start and disk[k].end == b.parts[k].end
            for k in b.parts)
        b.out.append("== verify")
        if same:
            b.out.append(f"disk matches memory: {len(disk)} partitions, {count} records")
        else:
            b.out.append("disk differs from memory")
    print("\n".join(b.out))


main()
