"""The oracle for mini_roaring: the same jobs over plain Python sets.

A bitmap here is a set of u32 values plus the set of chunk keys (value >>
16) held as run containers; every container type follows from the rules
the README states, so this file checks the Kāra port's containers and
bytes without being a roaring implementation itself.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os
import struct
import zlib

TOP = 1 << 32
ARRAY_MAX = 4096


class Bitmap:
    def __init__(self, values=(), runs=()):
        self.values = set(values)
        self.runs = set(runs)

    def chunks(self):
        out = {}
        for v in self.values:
            out.setdefault(v >> 16, []).append(v & 0xFFFF)
        for k in out:
            out[k].sort()
        return dict(sorted(out.items()))

    def kind(self, key, lows):
        if key in self.runs:
            return "run"
        return "array" if len(lows) <= ARRAY_MAX else "bitmap"


def runs_of(lows):
    out = []
    for v in lows:
        if out and out[-1][0] + out[-1][1] + 1 == v:
            out[-1][1] += 1
        else:
            out.append([v, 0])
    return out


def serialize(b):
    ch = b.chunks()
    keys = list(ch)
    n = len(keys)
    kinds = [b.kind(k, ch[k]) for k in keys]
    hasrun = "run" in kinds
    out = bytearray()
    if hasrun:
        out += struct.pack("<I", 12347 | ((n - 1) << 16))
        bits = bytearray((n + 7) // 8)
        for i, kd in enumerate(kinds):
            if kd == "run":
                bits[i // 8] |= 1 << (i % 8)
        out += bits
    else:
        out += struct.pack("<II", 12346, n)
    bodies = []
    for k, kd in zip(keys, kinds):
        lows = ch[k]
        out += struct.pack("<HH", k, len(lows) - 1)
        if kd == "array":
            bodies.append(b"".join(struct.pack("<H", v) for v in lows))
        elif kd == "bitmap":
            words = [0] * 1024
            for v in lows:
                words[v >> 6] |= 1 << (v & 63)
            bodies.append(b"".join(struct.pack("<Q", w) for w in words))
        else:
            rs = runs_of(lows)
            bodies.append(struct.pack("<H", len(rs)) + b"".join(struct.pack("<HH", s, l) for s, l in rs))
    if not hasrun or n >= 4:
        pos = len(out) + 4 * n
        for body in bodies:
            out += struct.pack("<I", pos)
            pos += len(body)
    for body in bodies:
        out += body
    return bytes(out)


class Bad(Exception):
    pass


def deserialize(data):
    def need(pos, k, what):
        if pos + k > len(data):
            raise Bad(f"truncated {what}")

    need(0, 4, "header")
    cookie = struct.unpack_from("<I", data, 0)[0]
    pos = 4
    runbits = None
    if cookie & 0xFFFF == 12347:
        n = (cookie >> 16) + 1
        need(pos, (n + 7) // 8, "header")
        runbits = data[pos:pos + (n + 7) // 8]
        pos += (n + 7) // 8
    elif cookie == 12346:
        need(pos, 4, "header")
        n = struct.unpack_from("<I", data, pos)[0]
        pos += 4
    else:
        raise Bad(f"bad cookie {cookie}")
    if n > 65536:
        raise Bad(f"{n} containers is more than 65536")
    need(pos, 4 * n, "header")
    heads = []
    for i in range(n):
        k, c = struct.unpack_from("<HH", data, pos + 4 * i)
        if heads and k <= heads[-1][0]:
            raise Bad(f"keys out of order at container {i}")
        heads.append((k, c + 1))
    pos += 4 * n
    offsets = None
    if runbits is None or n >= 4:
        need(pos, 4 * n, "header")
        offsets = [struct.unpack_from("<I", data, pos + 4 * i)[0] for i in range(n)]
        pos += 4 * n
    b = Bitmap()
    for i, (k, card) in enumerate(heads):
        if offsets is not None and offsets[i] != pos:
            raise Bad(f"offset of container {i} is {offsets[i]}, not {pos}")
        isrun = runbits is not None and runbits[i // 8] >> (i % 8) & 1
        if isrun:
            need(pos, 2, f"container {i}")
            nr = struct.unpack_from("<H", data, pos)[0]
            pos += 2
            need(pos, 4 * nr, f"container {i}")
            total = 0
            last = -1
            lows = []
            for j in range(nr):
                s, l = struct.unpack_from("<HH", data, pos + 4 * j)
                if s <= last or s + l > 65535:
                    raise Bad(f"bad run in container {i}")
                last = s + l
                total += l + 1
                lows.extend(range(s, s + l + 1))
            pos += 4 * nr
            if total != card:
                raise Bad(f"container {i} holds {total} values, its header says {card}")
            b.runs.add(k)
        elif card <= ARRAY_MAX:
            need(pos, 2 * card, f"container {i}")
            lows = [struct.unpack_from("<H", data, pos + 2 * j)[0] for j in range(card)]
            pos += 2 * card
            if any(lows[j] >= lows[j + 1] for j in range(len(lows) - 1)):
                raise Bad(f"unsorted array in container {i}")
        else:
            need(pos, 8192, f"container {i}")
            lows = []
            for w in range(1024):
                word = struct.unpack_from("<Q", data, pos + 8 * w)[0]
                for bit in range(64):
                    if word >> bit & 1:
                        lows.append(w * 64 + bit)
            pos += 8192
            if len(lows) != card:
                raise Bad(f"container {i} holds {len(lows)} values, its header says {card}")
        b.values.update((k << 16) | v for v in lows)
    if pos != len(data):
        raise Bad(f"{len(data) - pos} bytes after the last container")
    return b


def counts(b):
    ch = b.chunks()
    c = {"array": 0, "bitmap": 0, "run": 0}
    for k, lows in ch.items():
        c[b.kind(k, lows)] += 1
    return len(ch), c


def changed_chunks(before, after):
    """The chunk keys whose values differ between two value sets."""
    diff = before ^ after
    return {v >> 16 for v in diff}


def mutate(b, new_values, made_runs=()):
    """Sets b's values; a chunk whose values changed is no longer a run,
    except the chunks in made_runs; empty chunks go."""
    ch = changed_chunks(b.values, new_values)
    b.runs -= ch
    b.values = new_values
    present = {v >> 16 for v in new_values}
    b.runs |= set(made_runs) & present
    b.runs &= present


def optimize(b):
    b.runs = set()
    for k, lows in b.chunks().items():
        nr = len(runs_of(lows))
        size_run = 2 + 4 * nr
        size_other = min(2 * len(lows), 8192)
        if size_run < size_other:
            b.runs.add(k)


def parse_u32(s, allow_top=False):
    try:
        if not s or not all(c in "0123456789" for c in s):
            raise ValueError
        v = int(s)
    except ValueError:
        raise Bad(f"bad value: {s}")
    limit = TOP if allow_top else TOP - 1
    if v > limit:
        raise Bad(f"bad value: {s}")
    return v


def load_events(name):
    with open(os.path.join("data", name), encoding="utf-8", newline="") as fh:
        text = fh.read()
    sets = {}
    good = 0
    bad = 0
    for line in text.split("\n")[1:]:
        if not line:
            continue
        parts = line.split(",")
        ok = len(parts) == 3
        if ok:
            day, user, ev = parts
            ok = day in ("1", "2", "3", "4", "5", "6", "7") and ev in ("view", "signup", "cart", "buy")
            if ok:
                try:
                    u = parse_u32(user)
                except Bad:
                    ok = False
        if not ok:
            bad += 1
            continue
        good += 1
        sets.setdefault("d" + day, set()).add(u)
        sets.setdefault("e_" + ev, set()).add(u)
    return good, bad, sets


def show(name, b, out):
    if not b.values:
        out.append(f"{name}: empty")
        return
    vs = sorted(b.values)
    out.append(f"{name}: card={len(vs)} min={vs[0]} max={vs[-1]}")
    n, c = counts(b)
    out.append(f"  containers: {n} (array {c['array']}, bitmap {c['bitmap']}, run {c['run']})")
    parts = []
    for i, (k, lows) in enumerate(b.chunks().items()):
        if i == 6:
            parts.append("...")
            break
        parts.append(f"{k}:{b.kind(k, lows)}:{len(lows)}")
    out.append("  " + " ".join(parts))
    first = " ".join(str(v) for v in vs[:8])
    out.append("  first: " + first + (" ..." if len(vs) > 8 else ""))


def stats_line(name, b):
    n, c = counts(b)
    return (f"{name}: card={len(b.values)} containers={n} array={c['array']} "
            f"bitmap={c['bitmap']} run={c['run']} bytes={len(serialize(b))}")


def hexdump(b, out):
    data = serialize(b)
    for i in range(0, min(len(data), 64), 16):
        row = " ".join(f"{x:02x}" for x in data[i:i + 16])
        out.append(f"  {i:04x}: {row}")
    more = " (first 64 shown)" if len(data) > 64 else ""
    out.append(f"  {len(data)} bytes{more}")


def per_mille(k, n):
    return k * 1000 // n


def run_job(line, maps, out):
    w = line.split()
    cmd = w[0]
    args = w[1:]

    def get(name):
        if name not in maps:
            raise Bad(f"no bitmap named {name}")
        return maps[name]

    def need(k):
        if len(args) < k:
            raise Bad(f"{cmd}: needs {k} argument{'s' if k > 1 else ''}")

    if cmd == "load":
        need(1)
        good, bad, sets = load_events(args[0])
        out.append(f"loaded {args[0]}: {good} rows, {bad} skipped, {len(sets)} bitmaps")
        for k in sorted(sets):
            maps[k] = Bitmap(sets[k])
            out.append(f"  {k}: {len(sets[k])} users")
    elif cmd == "show":
        need(1)
        show(args[0], get(args[0]), out)
    elif cmd == "stats":
        need(1)
        out.append(stats_line(args[0], get(args[0])))
    elif cmd in ("and", "or", "xor", "andnot"):
        need(1)
        srcs = [get(a) for a in args[1:]]
        if not srcs:
            acc = set()
        else:
            acc = set(srcs[0].values)
            for s in srcs[1:]:
                if cmd == "and":
                    acc &= s.values
                elif cmd == "or":
                    acc |= s.values
                elif cmd == "xor":
                    acc ^= s.values
                else:
                    acc -= s.values
        maps[args[0]] = Bitmap(acc)
        out.append(f"{args[0]} = {cmd}({', '.join(args[1:])}): card={len(acc)}")
    elif cmd in ("addrange", "removerange", "flip"):
        need(3)
        lo = parse_u32(args[1], True)
        hi = parse_u32(args[2], True)
        b = maps.setdefault(args[0], Bitmap())
        before = set(b.values)
        rng = set(range(lo, hi)) if lo < hi else set()
        if cmd == "addrange":
            present = {v >> 16 for v in before}
            new = before | rng
            made = {v >> 16 for v in rng} - present
            mutate(b, new, made)
            sign = "+="
        elif cmd == "removerange":
            mutate(b, before - rng)
            sign = "-="
        else:
            mutate(b, before ^ rng)
            sign = "^="
        out.append(f"{args[0]} {sign} [{lo}, {hi}): card={len(b.values)}")
    elif cmd in ("add", "remove"):
        need(2)
        vals = [parse_u32(a) for a in args[1:]]
        b = maps.setdefault(args[0], Bitmap())
        new = set(b.values)
        for v in vals:
            if cmd == "add":
                new.add(v)
            else:
                new.discard(v)
        mutate(b, new)
        sign = "+" if cmd == "add" else "-"
        out.append(f"{args[0]} {sign} {{{', '.join(str(v) for v in vals)}}}: card={len(b.values)}")
    elif cmd == "optimize":
        need(1)
        b = get(args[0])
        optimize(b)
        _, c = counts(b)
        out.append(f"{args[0]} optimized: array {c['array']}, bitmap {c['bitmap']}, run {c['run']}")
    elif cmd == "rank":
        need(2)
        b = get(args[0])
        v = parse_u32(args[1])
        out.append(f"rank({args[0]}, {v}) = {sum(1 for x in b.values if x <= v)}")
    elif cmd == "select":
        need(2)
        b = get(args[0])
        i = parse_u32(args[1])
        if i >= len(b.values):
            out.append(f"! select({args[0]}, {i}): out of range (card {len(b.values)})")
        else:
            out.append(f"select({args[0]}, {i}) = {sorted(b.values)[i]}")
    elif cmd == "contains":
        need(2)
        b = get(args[0])
        parts = []
        for a in args[1:]:
            v = parse_u32(a)
            parts.append(f"{v} {'yes' if v in b.values else 'no'}")
        out.append(f"contains {args[0]}: {', '.join(parts)}")
    elif cmd == "retention":
        need(2)
        a, b = get(args[0]), get(args[1])
        k = len(a.values & b.values)
        n = len(a.values)
        if n == 0:
            out.append(f"retention {args[0]} -> {args[1]}: kept 0 of 0")
        else:
            out.append(f"retention {args[0]} -> {args[1]}: kept {k} of {n} ({per_mille(k, n)} per mille)")
    elif cmd == "jaccard":
        need(2)
        a, b = get(args[0]), get(args[1])
        u = len(a.values | b.values)
        if u == 0:
            out.append(f"jaccard({args[0]}, {args[1]}) undefined: both empty")
        else:
            out.append(f"jaccard({args[0]}, {args[1]}) = {per_mille(len(a.values & b.values), u)} per mille")
    elif cmd == "equal":
        need(2)
        a, b = get(args[0]), get(args[1])
        out.append(f"{args[0]} == {args[1]}: {'yes' if a.values == b.values else 'no'}")
    elif cmd == "hexdump":
        need(1)
        out.append(f"{args[0]}:")
        hexdump(get(args[0]), out)
    elif cmd == "save":
        need(2)
        data = serialize(get(args[0]))
        with open(os.path.join("data", args[1]), "wb") as fh:
            fh.write(data)
        out.append(f"saved {args[0]} -> {args[1]}: {len(data)} bytes, crc32 {zlib.crc32(data):08x}")
    elif cmd == "loadroar":
        need(2)
        path = os.path.join("data", args[1])
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            raise Bad(f"{args[1]}: cannot read")
        try:
            b = deserialize(data)
        except Bad as e:
            raise Bad(f"{args[1]}: {e}")
        maps[args[0]] = b
        n, c = counts(b)
        out.append(f"loaded {args[0]} <- {args[1]}: card={len(b.values)} containers={n} "
                   f"(array {c['array']}, bitmap {c['bitmap']}, run {c['run']})")
    else:
        raise Bad(f"unknown command: {cmd}")


def main():
    with open(os.path.join("data", "jobs.txt"), encoding="utf-8", newline="") as fh:
        jobs = fh.read()
    maps = {}
    out = []
    for line in jobs.split("\n"):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        out.append(f"> {t}")
        try:
            run_job(t, maps, out)
        except Bad as e:
            out.append(f"! {e}")
    print("\n".join(out))


main()
