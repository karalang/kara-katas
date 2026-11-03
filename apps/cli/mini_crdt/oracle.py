"""The oracle for mini_crdt: the same replicas, written plainly in Python.

It follows the README's rules for the four data types, causal delivery,
Lamport clocks and the op log, so the Kāra port's output and log files
must match it byte for byte.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os


class Fail(Exception):
    pass


def fmt_id(i):
    return f"{i[0]}@{i[1]}"


def parse_id(s):
    c, o = s.split("@")
    return (int(c), o)


class Op:
    def __init__(self, origin, seq, lamport, vc, typ, obj, kind, payload):
        self.origin = origin
        self.seq = seq
        self.lamport = lamport
        self.vc = vc  # dict replica -> count, every replica present
        self.typ = typ
        self.obj = obj
        self.kind = kind
        self.payload = payload  # list of words; for an insert [after, text]

    def span(self):
        return len(self.payload[1]) if self.kind == "insert" else 1

    def line(self, names):
        vc = ",".join(f"{n}:{self.vc[n]}" for n in names)
        return " ".join(["op", self.origin, str(self.seq), str(self.lamport), vc,
                         self.typ, self.obj, self.kind] + self.payload)

    @staticmethod
    def parse(text):
        w = text.split(" ")
        vc = {}
        for part in w[4].split(","):
            k, v = part.split(":")
            vc[k] = int(v)
        if w[7] == "insert":
            payload = [w[8], " ".join(w[9:])]
        else:
            payload = w[8:]
        return Op(w[1], int(w[2]), int(w[3]), vc, w[5], w[6], w[7], payload)


class Replica:
    def __init__(self, name, names, logdir):
        self.name = name
        self.names = names
        self.path = os.path.join(logdir, name + ".log")
        self.alive = True
        self.reset()

    def reset(self):
        self.clock = 0
        self.vv = {n: 0 for n in self.names}
        self.ops = []  # applied, in order
        self.counters = {}
        self.sets = {}  # obj -> elem -> set of tags
        self.regs = {}  # obj -> (stamp, value)
        self.texts = {}  # obj -> list of [id, ch, deleted]

    # ------------------------------------------------------------ apply

    def apply(self, op, log=True):
        if op.typ == "counter":
            self.counters[op.obj] = self.counters.get(op.obj, 0) + int(op.payload[0])
        elif op.typ == "set":
            elems = self.sets.setdefault(op.obj, {})
            e = op.payload[0]
            if op.kind == "add":
                elems.setdefault(e, set()).add(f"{op.origin}.{op.seq}")
            else:
                gone = set(op.payload[1].split(","))
                if e in elems:
                    elems[e] -= gone
        elif op.typ == "reg":
            stamp = (op.lamport, op.origin)
            cur = self.regs.get(op.obj)
            if cur is None or stamp > cur[0]:
                self.regs[op.obj] = (stamp, op.payload[0])
        else:
            seqs = self.texts.setdefault(op.obj, [])
            if op.kind == "insert":
                after, text = op.payload
                if after == "root":
                    i = 0
                else:
                    a = parse_id(after)
                    i = next(k for k, el in enumerate(seqs) if el[0] == a) + 1
                for k, ch in enumerate(text):
                    nid = (op.lamport + k, op.origin)
                    while i < len(seqs) and seqs[i][0] > nid:
                        i += 1
                    seqs.insert(i, [nid, ch, False])
                    i += 1
            else:
                ids = {parse_id(x) for x in op.payload[0].split(",")}
                for el in seqs:
                    if el[0] in ids:
                        el[2] = True
        self.clock = max(self.clock, op.lamport + op.span() - 1)
        self.vv[op.origin] = op.seq
        self.ops.append(op)
        if log:
            with open(self.path, "a", encoding="utf-8", newline="") as fh:
                fh.write(op.line(self.names) + "\n")

    # ------------------------------------------------------------ views

    def visible(self, obj):
        return [el for el in self.texts.get(obj, []) if not el[2]]

    def text_of(self, obj):
        return "".join(el[1] for el in self.visible(obj))

    def set_of(self, obj):
        return sorted(e for e, tags in self.sets.get(obj, {}).items() if tags)

    def show_lines(self):
        out = []
        for k in sorted(self.counters):
            out.append(f"  counter {k} = {self.counters[k]}")
        for k in sorted(self.regs):
            (lam, who), v = self.regs[k]
            out.append(f"  reg {k} = {v} ({who}@{lam})")
        for k in sorted(self.sets):
            out.append(f"  set {k} = {{{', '.join(self.set_of(k))}}}")
        for k in sorted(self.texts):
            all_ = self.texts[k]
            vis = self.visible(k)
            out.append(f"  text {k} = \"{self.text_of(k)}\" "
                       f"({len(vis)} visible, {len(all_) - len(vis)} deleted)")
        return out

    # ------------------------------------------------------------ local ops

    def make(self, typ, obj, kind, payload, span):
        seq = self.vv[self.name] + 1
        vc = dict(self.vv)
        vc[self.name] = seq
        op = Op(self.name, seq, self.clock + 1, vc, typ, obj, kind, payload)
        assert op.span() == span
        self.apply(op)
        return op

    def local(self, w):
        """One edit line; returns the event text."""
        typ, obj, kind = w[1], w[2], w[3]
        args = w[4:]
        if typ == "counter":
            n = int(args[0])
            self.make(typ, obj, kind, [str(n)], 1)
            sign = "+" if n >= 0 else ""
            return f"{obj} {sign}{n} -> {self.counters[obj]}"
        if typ == "set":
            e = args[0]
            if kind == "add":
                self.make(typ, obj, kind, [e], 1)
                return f"{obj} add {e} -> {{{', '.join(self.set_of(obj))}}}"
            tags = self.sets.get(obj, {}).get(e, set())
            if not tags:
                raise Fail(f"{obj} remove {e}: not in the set")
            n = len(tags)
            self.make(typ, obj, kind, [e, ",".join(sorted(tags))], 1)
            return (f"{obj} remove {e} ({n} add{'s' if n != 1 else ''}) -> "
                    f"{{{', '.join(self.set_of(obj))}}}")
        if typ == "reg":
            op = self.make(typ, obj, kind, [args[0]], 1)
            return f"{obj} = {args[0]} ({self.name}@{op.lamport})"
        vis = self.visible(obj)
        if kind == "insert":
            pos = int(args[0])
            text = " ".join(args[1:])
            if pos > len(vis):
                raise Fail(f"{obj} insert at {pos}: only {len(vis)} chars")
            after = "root" if pos == 0 else fmt_id(vis[pos - 1][0])
            self.make(typ, obj, kind, [after, text], len(text))
            return f"{obj} insert \"{text}\" at {pos} -> \"{self.text_of(obj)}\""
        pos, n = int(args[0]), int(args[1])
        if pos + n > len(vis):
            raise Fail(f"{obj} delete {pos}..{pos + n}: only {len(vis)} chars")
        ids = ",".join(fmt_id(el[0]) for el in vis[pos:pos + n])
        self.make(typ, obj, kind, [ids], 1)
        return f"{obj} delete {pos}..{pos + n} -> \"{self.text_of(obj)}\""


def causal_key(op):
    return (sum(op.vc.values()), op.origin, op.seq)


def plural(n):
    return f"{n} op" if n == 1 else f"{n} ops"


class Session:
    def __init__(self, stem, names):
        self.names = names
        self.logdir = os.path.join("data", "run", stem)
        os.makedirs(self.logdir, exist_ok=True)
        self.reps = {}
        for n in names:
            r = Replica(n, names, self.logdir)
            with open(r.path, "w", encoding="utf-8", newline=""):
                pass
            self.reps[n] = r
        self.out = []

    def deliver(self, src, dst):
        missing = [op for op in src.ops if dst.vv[op.origin] < op.seq]
        missing.sort(key=causal_key)
        for op in missing:
            dst.apply(op)
        return missing

    def run(self, w):
        cmd = w[0]
        if cmd == "sync":
            if w[1] == "all":
                live = [self.reps[n] for n in self.names if self.reps[n].alive]
                pool = {}
                for r in live:
                    for op in r.ops:
                        pool[(op.origin, op.seq)] = op
                parts = []
                for n in self.names:
                    r = self.reps[n]
                    if not r.alive:
                        parts.append(f"{n} down")
                        continue
                    missing = [op for op in pool.values() if r.vv[op.origin] < op.seq]
                    missing.sort(key=causal_key)
                    for op in missing:
                        r.apply(op)
                    parts.append(f"{n} +{len(missing)}")
                self.out.append("sync all: " + ", ".join(parts))
                return
            a, b = self.reps[w[1]], self.reps[w[2]]
            for r in (a, b):
                if not r.alive:
                    self.out.append(f"sync {a.name} -> {b.name}: {r.name} is down")
                    return
            got = self.deliver(a, b)
            if not got:
                self.out.append(f"sync {a.name} -> {b.name}: up to date")
                return
            by = {}
            for op in got:
                by[op.origin] = by.get(op.origin, 0) + 1
            detail = " ".join(f"{k}:{by[k]}" for k in self.names if k in by)
            self.out.append(f"sync {a.name} -> {b.name}: {plural(len(got))} ({detail})")
        elif cmd == "show":
            r = self.reps[w[1]]
            if not r.alive:
                self.out.append(f"show {r.name}: down")
                return
            self.out.append(f"show {r.name}: clock {r.clock}, {plural(len(r.ops))}")
            self.out.extend(r.show_lines())
        elif cmd == "check":
            live = [self.reps[n] for n in self.names if self.reps[n].alive]
            groups = []
            for r in live:
                view = r.show_lines()
                for g in groups:
                    if g[0] == view:
                        g[1].append(r.name)
                        break
                else:
                    groups.append((view, [r.name]))
            if len(groups) == 1:
                self.out.append(f"check: converged ({' '.join(groups[0][1])})")
            else:
                self.out.append("check: " + str(len(groups)) + " states: "
                                + " | ".join(" ".join(g[1]) for g in groups))
        elif cmd == "crash":
            r = self.reps[w[1]]
            if not r.alive:
                raise Fail(f"{r.name} is already down")
            r.alive = False
            r.reset()
            self.out.append(f"{r.name} crashes")
        elif cmd == "restart":
            r = self.reps[w[1]]
            if r.alive:
                raise Fail(f"{r.name} is not down")
            with open(r.path, encoding="utf-8", newline="") as fh:
                data = fh.read()
            n = 0
            for line in data.split("\n"):
                if line:
                    r.apply(Op.parse(line), log=False)
                    n += 1
            r.alive = True
            self.out.append(f"{r.name} restarts: {plural(n)} replayed from {r.name}.log "
                            f"({len(data.encode())} bytes), clock {r.clock}")
        else:
            r = self.reps[w[0]]
            if not r.alive:
                raise Fail(f"{r.name} is down")
            self.out.append(f"{r.name}: " + r.local(w))

    def summary(self):
        out = ["-- end"]
        for n in self.names:
            r = self.reps[n]
            size = os.path.getsize(r.path)
            if not r.alive:
                out.append(f"  {n}: down, log {size} bytes")
                continue
            own = sum(1 for op in r.ops if op.origin == n)
            out.append(f"  {n}: {plural(len(r.ops))} ({own} own), clock {r.clock}, log {size} bytes")
        return out


TYPES = {"counter": ("add",), "set": ("add", "remove"), "reg": ("set",),
         "text": ("insert", "delete")}


def is_int(s):
    t = s[1:] if s.startswith("-") else s
    return t.isdigit()


def parse(name, text):
    names = []
    types = {}
    lines = []
    errs = []
    for no, line in enumerate(text.split("\n"), 1):
        if line == "" or line.startswith("#"):
            continue
        w = line.split(" ")
        try:
            if w[0] == "replicas":
                if names:
                    raise Fail("replicas given twice")
                if len(w) < 2 or len(set(w[1:])) != len(w) - 1:
                    raise Fail("replicas needs distinct names")
                names = w[1:]
                continue
            if not names:
                raise Fail("the replicas line must come first")
            if w[0] in ("sync", "show", "crash", "restart", "check"):
                want = {"sync": 3, "show": 2, "crash": 2, "restart": 2, "check": 1}[w[0]]
                if w[0] == "sync" and len(w) == 2 and w[1] == "all":
                    lines.append(w)
                    continue
                if len(w) != want:
                    raise Fail(f"{w[0]} takes {want - 1} argument{'s' if want != 2 else ''}")
                for r in w[1:]:
                    if r not in names:
                        raise Fail(f"no replica {r}")
                lines.append(w)
                continue
            if w[0] not in names:
                raise Fail(f"no replica {w[0]}")
            if len(w) < 4:
                raise Fail("an edit is: replica type object action ...")
            typ, obj, kind = w[1], w[2], w[3]
            if typ not in TYPES:
                raise Fail(f"unknown type {typ}")
            if kind not in TYPES[typ]:
                raise Fail(f"a {typ} has no {kind}")
            if types.get(obj, typ) != typ:
                raise Fail(f"{obj} is a {types[obj]}, not a {typ}")
            args = w[4:]
            if typ == "counter" and not (len(args) == 1 and is_int(args[0])):
                raise Fail("add needs a whole number")
            if typ in ("set", "reg") and len(args) != 1:
                raise Fail("a value is one word")
            if kind == "insert" and (len(args) < 2 or not args[0].isdigit()):
                raise Fail("insert needs a position and text")
            if kind == "delete" and not (len(args) == 2 and args[0].isdigit()
                                         and args[1].isdigit() and int(args[1]) > 0):
                raise Fail("delete needs a position and a count")
            types[obj] = typ
            lines.append(w)
        except Fail as e:
            errs.append(f"{name} line {no}: {e}")
    if not names:
        errs.append(f"{name}: no replicas line")
    return names, lines, errs


def run(name, text):
    names, lines, errs = parse(name, text)
    out = [f"== {name}: replicas {' '.join(names)}"]
    if errs:
        return out + ["! " + e for e in errs]
    s = Session(name.split(".")[0], names)
    for w in lines:
        try:
            s.run(w)
        except Fail as e:
            s.out.append(f"! {e}")
    return out + s.out + s.summary()


def main():
    names = sorted(x for x in os.listdir("data") if x.endswith(".crdt"))
    out = []
    for name in names:
        with open(os.path.join("data", name), encoding="utf-8", newline="") as fh:
            out += run(name, fh.read())
    print("\n".join(out))


main()
