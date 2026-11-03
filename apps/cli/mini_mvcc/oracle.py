"""The oracle for mini_mvcc: the same store, written plainly in Python.

It follows the README's rules for snapshots, the three isolation
levels, commit validation, vacuum, the write-ahead log, recovery and
checkpoints, so the Kāra port's output and its log and snapshot files
must match it byte for byte.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os

LEVELS = ("rc", "si", "ser")
SESSION_CMDS = ("dump", "vacuum", "crash", "recover", "checkpoint")
ACTIONS = {
    "get": (1, "get takes a key"),
    "del": (1, "del takes a key"),
    "put": (2, "put takes a key and a value"),
    "add": (2, "add takes a key and a whole number"),
    "scan": (1, "scan takes a prefix"),
    "sum": (1, "sum takes a prefix"),
    "commit": (0, "commit takes no arguments"),
    "abort": (0, "abort takes no arguments"),
}


class Fail(Exception):
    pass


def is_digits(s):
    return len(s) > 0 and all("0" <= c <= "9" for c in s)


def is_int(s):
    return is_digits(s[1:]) if s.startswith("-") else is_digits(s)


def fnv(b):
    h = 0x811C9DC5
    for c in b:
        h ^= c
        h = (h * 0x01000193) % 4294967296
    return h


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def record(header, body):
    text = header + "\n" + "".join(l + "\n" for l in body)
    return text + f"end {fnv(text.encode()):08x}\n"


class Txn:
    def __init__(self, name, level, read_ts):
        self.name = name
        self.level = level
        self.read_ts = read_ts
        self.writes = {}
        self.reads = set()
        self.prefixes = set()


class Store:
    def __init__(self, stem):
        self.stem = stem
        self.wal = os.path.join("data", "run", stem + ".wal")
        self.snap = os.path.join("data", "run", stem + ".snap")
        for p in (self.wal, self.snap, self.snap + ".tmp"):
            if os.path.exists(p):
                os.remove(p)
        open(self.wal, "wb").close()
        self.versions = {}
        self.clock = 0
        self.txns = {}
        self.down = False
        self.commits = 0
        self.aborts = 0
        self.out = []

    # ---------------------------------------------------------- reading
    def newest(self, key):
        vs = self.versions.get(key)
        return vs[-1] if vs else None

    def visible(self, key, ts):
        for v in reversed(self.versions.get(key, [])):
            if v[0] <= ts:
                return v[2]
        return None

    def snap_ts(self, t):
        return self.clock if t.level == "rc" else t.read_ts

    def read(self, t, key):
        if key in t.writes:
            return t.writes[key]
        t.reads.add(key)
        return self.visible(key, self.snap_ts(t))

    def range(self, t, p):
        t.prefixes.add(p)
        ts = self.snap_ts(t)
        seen = {}
        for k in self.versions:
            if k.startswith(p):
                v = self.visible(k, ts)
                if v is not None:
                    seen[k] = v
        for k, v in t.writes.items():
            if k.startswith(p):
                if v is None:
                    seen.pop(k, None)
                else:
                    seen[k] = v
        return sorted(seen.items())

    # ---------------------------------------------------------- the log
    def append(self, text):
        with open(self.wal, "ab") as fh:
            fh.write(text.encode())

    def install(self, ts, name, writes):
        for k in sorted(writes):
            self.versions.setdefault(k, []).append((ts, name, writes[k]))

    def vacuum_at(self, h):
        removed = 0
        gone = 0
        for k in sorted(self.versions):
            vs = self.versions[k]
            keep = [v for v in vs if v[0] > h]
            old = [v for v in vs if v[0] <= h]
            if old and old[-1][2] is not None:
                keep.insert(0, old[-1])
            removed += len(vs) - len(keep)
            if keep:
                self.versions[k] = keep
            else:
                del self.versions[k]
                gone += 1
        return removed, gone

    # ---------------------------------------------------------- commands
    def run(self, w):
        cmd = w[0]
        if cmd == "tear":
            if not self.down:
                raise Fail("tear needs a crashed store")
            with open(self.wal, "rb") as fh:
                b = fh.read()
            keep = max(0, len(b) - int(w[1]))
            with open(self.wal, "wb") as fh:
                fh.write(b[:keep])
            self.out.append(f"tear {w[1]}: wal {len(b)} -> {keep} bytes")
            return
        if cmd == "recover":
            if not self.down:
                raise Fail("the store is up")
            self.recover()
            return
        if self.down:
            raise Fail("the store is down")
        if cmd == "begin":
            name = w[1]
            if name in self.txns:
                raise Fail(f"{name} is already active")
            level = w[2] if len(w) == 3 else "si"
            t = Txn(name, level, self.clock)
            self.txns[name] = t
            if level == "rc":
                self.out.append(f"{name} begin rc")
            else:
                self.out.append(f"{name} begin {level} at {self.clock}")
            return
        if cmd == "dump":
            self.out.append(f"dump at clock {self.clock}:")
            if not self.versions:
                self.out.append("  (empty)")
            for k in sorted(self.versions):
                vs = " ".join(f"@{v[0]} {v[2] if v[2] is not None else '-'}" for v in self.versions[k])
                self.out.append(f"  {k} {vs}")
            return
        if cmd == "vacuum":
            h = self.clock
            for t in self.txns.values():
                if t.level != "rc" and t.read_ts < h:
                    h = t.read_ts
            removed, gone = self.vacuum_at(h)
            self.append(record(f"vacuum {h}", []))
            self.out.append(f"vacuum at horizon {h}: removed {plural(removed, 'version')}, "
                            f"{plural(gone, 'key')} gone")
            return
        if cmd == "crash":
            lost = list(self.txns)
            self.out.append("crash: lost " + " ".join(lost) if lost else "crash: no open transactions")
            self.versions = {}
            self.clock = 0
            self.txns = {}
            self.down = True
            return
        if cmd == "checkpoint":
            n = sum(len(vs) for vs in self.versions.values())
            lines = [f"snapshot {self.clock} {n}"]
            for k in sorted(self.versions):
                for v in self.versions[k]:
                    lines.append(f"v {k} {v[0]} {v[1]} {v[2] if v[2] is not None else '-'}")
            with open(self.snap + ".tmp", "wb") as fh:
                fh.write(("\n".join(lines) + "\n").encode())
            os.replace(self.snap + ".tmp", self.snap)
            size = os.path.getsize(self.wal)
            open(self.wal, "wb").close()
            self.out.append(f"checkpoint at clock {self.clock}: {plural(n, 'version')}, wal {size} -> 0 bytes")
            return
        name = cmd
        t = self.txns.get(name)
        if t is None:
            raise Fail(f"{name} is not active")
        act = w[1]
        if act == "get":
            v = self.read(t, w[2])
            self.out.append(f"{name} get {w[2]} = {v if v is not None else '(none)'}")
        elif act == "put":
            t.writes[w[2]] = w[3]
            self.out.append(f"{name} put {w[2]} {w[3]}")
        elif act == "del":
            t.writes[w[2]] = None
            self.out.append(f"{name} del {w[2]}")
        elif act == "add":
            v = self.read(t, w[2])
            if v is not None and not is_int(v):
                self.kill(name)
                raise Fail(f'{name} add {w[2]}: "{v}" is not a number; {name} aborted')
            cur = int(v) if v is not None else 0
            new = cur + int(w[3])
            t.writes[w[2]] = str(new)
            self.out.append(f"{name} add {w[2]} {w[3]}: {cur} -> {new}")
        elif act == "scan":
            items = self.range(t, w[2])
            shown = " ".join(f"{k}={v}" for k, v in items) if items else "(none)"
            self.out.append(f"{name} scan {w[2]} -> {shown}")
        elif act == "sum":
            items = self.range(t, w[2])
            total = 0
            for k, v in items:
                if not is_int(v):
                    self.kill(name)
                    raise Fail(f'{name} sum {w[2]}: {k} is "{v}", not a number; {name} aborted')
                total += int(v)
            self.out.append(f"{name} sum {w[2]} = {total} over {plural(len(items), 'key')}")
        elif act == "abort":
            self.kill(name)
            self.out.append(f"{name} abort")
        else:
            self.commit(t)

    def kill(self, name):
        del self.txns[name]
        self.aborts += 1

    def conflict(self, t):
        if t.level == "rc":
            return None
        for k in sorted(t.writes):
            v = self.newest(k)
            if v is not None and v[0] > t.read_ts:
                return f"write-write conflict on {k} ({v[1]} committed it at {v[0]})"
        if t.level != "ser":
            return None
        for k in sorted(t.reads):
            v = self.newest(k)
            if v is not None and v[0] > t.read_ts:
                return f"read-write conflict on {k} ({v[1]} committed it at {v[0]})"
        for p in sorted(t.prefixes):
            for k in sorted(self.versions):
                v = self.newest(k)
                if k.startswith(p) and v[0] > t.read_ts:
                    return f"phantom under {p} ({v[1]} committed {k} at {v[0]})"
        return None

    def commit(self, t):
        if not t.writes:
            del self.txns[t.name]
            self.commits += 1
            self.out.append(f"{t.name} commit (read-only)")
            return
        why = self.conflict(t)
        if why is not None:
            self.kill(t.name)
            self.out.append(f"{t.name} abort: {why}")
            return
        self.clock += 1
        body = []
        for k in sorted(t.writes):
            v = t.writes[k]
            body.append(f"put {k} {v}" if v is not None else f"del {k}")
        self.append(record(f"commit {self.clock} {t.name} {len(body)}", body))
        self.install(self.clock, t.name, t.writes)
        del self.txns[t.name]
        self.commits += 1
        self.out.append(f"{t.name} commit at {self.clock} ({plural(len(body), 'write')})")

    # ---------------------------------------------------------- recovery
    def recover(self):
        if os.path.exists(self.snap):
            with open(self.snap, "rb") as fh:
                lines = fh.read().decode().split("\n")
            head = lines[0].split(" ")
            self.clock = int(head[1])
            for l in lines[1:]:
                if not l:
                    continue
                w = l.split(" ")
                self.versions.setdefault(w[1], []).append((int(w[2]), w[3], None if w[4] == "-" else w[4]))
            self.out.append(f"recover: snapshot at clock {self.clock}, {plural(int(head[2]), 'version')}")
        with open(self.wal, "rb") as fh:
            data = fh.read().decode()
        pos = 0
        commits = 0
        vacuums = 0
        while pos < len(data):
            r = parse_record(data, pos)
            if r is None:
                break
            pos, rec = r
            if rec[0] == "commit":
                _, ts, name, writes = rec
                self.clock = ts
                self.install(ts, name, writes)
                commits += 1
            else:
                self.vacuum_at(rec[1])
                vacuums += 1
        self.out.append(f"recover: replayed {plural(commits, 'commit')} and {plural(vacuums, 'vacuum')}, "
                        f"clock {self.clock}")
        if pos < len(data):
            self.out.append(f"recover: dropped a torn record at byte {pos} ({plural(len(data) - pos, 'byte')})")
            with open(self.wal, "wb") as fh:
                fh.write(data[:pos].encode())
        self.down = False

    def summary(self):
        out = []
        if self.txns:
            out.append("open at end: " + " ".join(self.txns))
        n = sum(len(vs) for vs in self.versions.values())
        out.append(f"stats: {plural(self.commits, 'commit')}, {plural(self.aborts, 'abort')}, "
                   f"clock {self.clock}, {plural(len(self.versions), 'key')}, {plural(n, 'version')}, "
                   f"wal {os.path.getsize(self.wal)} bytes")
        return out


def parse_record(data, pos):
    def line(p):
        i = data.find("\n", p)
        return None if i < 0 else (data[p:i], i + 1)

    r = line(pos)
    if r is None:
        return None
    head, p = r
    w = head.split(" ")
    if w[0] == "commit" and len(w) == 4 and is_digits(w[1]) and is_digits(w[3]):
        writes = {}
        for _ in range(int(w[3])):
            r = line(p)
            if r is None:
                return None
            b, p = r
            bw = b.split(" ")
            if bw[0] == "put" and len(bw) == 3:
                writes[bw[1]] = bw[2]
            elif bw[0] == "del" and len(bw) == 2:
                writes[bw[1]] = None
            else:
                return None
        rec = ("commit", int(w[1]), w[2], writes)
    elif w[0] == "vacuum" and len(w) == 2 and is_digits(w[1]):
        rec = ("vacuum", int(w[1]))
    else:
        return None
    r = line(p)
    if r is None:
        return None
    e, q = r
    if e != f"end {fnv(data[pos:p].encode()):08x}":
        return None
    return q, rec


def check_line(w, begun):
    cmd = w[0]
    if cmd == "begin":
        if len(w) not in (2, 3):
            raise Fail("begin takes a name and an optional level")
        begun.add(w[1])
        if len(w) == 3 and w[2] not in LEVELS:
            raise Fail(f"unknown level {w[2]}")
        return
    if cmd in SESSION_CMDS:
        if len(w) != 1:
            raise Fail(f"{cmd} takes no arguments")
        return
    if cmd == "tear":
        if len(w) != 2 or not is_digits(w[1]):
            raise Fail("tear needs a byte count")
        return
    if len(w) == 1:
        raise Fail(f"unknown command {cmd}")
    if cmd not in begun:
        raise Fail(f"{cmd} has no begin before this line")
    act = w[1]
    if act not in ACTIONS:
        raise Fail(f"unknown action {act}")
    n, msg = ACTIONS[act]
    if len(w) != n + 2:
        raise Fail(msg)
    if act == "put" and w[3] == "-":
        raise Fail("a value cannot be -")
    if act == "add" and not is_int(w[3]):
        raise Fail("add needs a whole number")


def run(name, text):
    out = [f"== {name}"]
    lines = []
    errs = []
    begun = set()
    for no, line in enumerate(text.split("\n"), 1):
        if not line or line.startswith("#"):
            continue
        w = line.split(" ")
        try:
            check_line(w, begun)
            lines.append(w)
        except Fail as e:
            errs.append(f"! {name} line {no}: {e}")
    if errs:
        return out + errs
    s = Store(name.split(".")[0])
    for w in lines:
        try:
            s.run(w)
        except Fail as e:
            s.out.append(f"! {e}")
    return out + s.out + s.summary()


def main():
    os.makedirs(os.path.join("data", "run"), exist_ok=True)
    out = []
    for name in sorted(os.listdir("data")):
        if name.endswith(".mvcc"):
            with open(os.path.join("data", name), encoding="utf-8") as fh:
                out += run(name, fh.read())
    print("\n".join(out))


main()
