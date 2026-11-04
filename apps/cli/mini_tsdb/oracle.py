"""The oracle for mini_tsdb: the same database, written plainly in Python.

It follows the README's rules for the scrape format, ingestion, the
Gorilla chunk encoding, the block files and the query language, so the
Kāra port's output and its block files must match it byte for byte.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os
import struct

T0 = 1700000000000
CHUNK = 120
LOOKBACK = 300000


class Fail(Exception):
    pass


def is_digits(s):
    return len(s) > 0 and all("0" <= c <= "9" for c in s)


def is_number(s):
    body = s[1:] if s.startswith("-") else s
    if "." in body:
        a, b = body.split(".", 1)
        return is_digits(a) and is_digits(b)
    return is_digits(body)


def is_name_start(c):
    return c.isascii() and (c.isalpha() or c in "_:")


def is_name_char(c):
    return is_name_start(c) or ("0" <= c <= "9")


def show(labels):
    name = labels.get("__name__", "")
    rest = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()) if k != "__name__")
    if name and not rest:
        return name
    return f"{name}{{{rest}}}"


def fmt(v):
    return f"{v:.4f}"


# ------------------------------------------------------------ scrapes

def parse_sample(line):
    i = 0
    while i < len(line) and is_name_char(line[i]) and (i > 0 or is_name_start(line[i])):
        i += 1
    if i == 0:
        raise Fail("missing metric name")
    labels = {"__name__": line[:i]}
    if i < len(line) and line[i] == "{":
        i += 1
        while True:
            if i < len(line) and line[i] == "}":
                i += 1
                break
            j = i
            while j < len(line) and is_name_char(line[j]):
                j += 1
            if j == i or j >= len(line) or line[j] != "=":
                raise Fail("bad label")
            key = line[i:j]
            if j + 1 >= len(line) or line[j + 1] != '"':
                raise Fail(f"the value of label {key} must be quoted")
            k = line.find('"', j + 2)
            if k < 0:
                raise Fail(f"the value of label {key} is not closed")
            labels[key] = line[j + 2:k]
            i = k + 1
            if i < len(line) and line[i] == ",":
                i += 1
            elif i < len(line) and line[i] == "}":
                continue
            else:
                raise Fail("bad label")
    rest = line[i:].split(" ")
    if not rest or rest[0] != "" or len(rest) < 2:
        raise Fail("expected a space and a value")
    rest = rest[1:]
    if not is_number(rest[0]):
        raise Fail(f'bad value "{rest[0]}"')
    if len(rest) < 2:
        raise Fail("missing timestamp")
    if len(rest) > 2 or not is_digits(rest[1]):
        raise Fail(f'bad timestamp "{" ".join(rest[1:])}"')
    return labels, float(rest[0]), int(rest[1])


def parse_file(text):
    out = []
    for no, line in enumerate(text.split("\n"), 1):
        if not line or line.startswith("#"):
            continue
        try:
            out.append((no, parse_sample(line), None))
        except Fail as e:
            out.append((no, None, str(e)))
    return out


# ------------------------------------------------------------ gorilla

class BitWriter:
    def __init__(self):
        self.bytes = bytearray()
        self.nbits = 0

    def bit(self, b):
        if self.nbits % 8 == 0:
            self.bytes.append(0)
        if b:
            self.bytes[-1] |= 0x80 >> (self.nbits % 8)
        self.nbits += 1

    def bits(self, v, n):
        for k in range(n - 1, -1, -1):
            self.bit((v >> k) & 1)


class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def bit(self):
        b = (self.data[self.pos // 8] >> (7 - self.pos % 8)) & 1
        self.pos += 1
        return b

    def bits(self, n):
        v = 0
        for _ in range(n):
            v = (v << 1) | self.bit()
        return v


def fbits(v):
    return struct.unpack(">Q", struct.pack(">d", v))[0]


def bitsf(b):
    return struct.unpack(">d", struct.pack(">Q", b))[0]


def clz(x):
    return 64 - x.bit_length()


def ctz(x):
    return (x & -x).bit_length() - 1


BUCKETS = [(2, 14), (3, 17), (4, 20)]


def encode(samples):
    w = BitWriter()
    w.bits(len(samples), 16)
    pt, pv = samples[0]
    w.bits(pt & 0xFFFFFFFFFFFFFFFF, 64)
    w.bits(fbits(pv), 64)
    pdelta = 0
    lead, trail = 0xFF, 0
    for t, v in samples[1:]:
        delta = t - pt
        dod = delta - pdelta
        if dod == 0:
            w.bit(0)
        else:
            for prefix, nb in BUCKETS:
                if -((1 << (nb - 1)) - 1) <= dod <= (1 << (nb - 1)):
                    w.bits((1 << prefix) - 2, prefix)
                    w.bits(dod & ((1 << nb) - 1), nb)
                    break
            else:
                w.bits(0b1111, 4)
                w.bits(dod & 0xFFFFFFFFFFFFFFFF, 64)
        x = fbits(v) ^ fbits(pv)
        if x == 0:
            w.bit(0)
        else:
            w.bit(1)
            l = min(clz(x), 31)
            tr = ctz(x)
            if lead != 0xFF and l >= lead and tr >= trail:
                w.bit(0)
                w.bits(x >> trail, 64 - lead - trail)
            else:
                lead, trail = l, tr
                w.bit(1)
                w.bits(l, 5)
                sig = 64 - l - tr
                w.bits(sig & 63, 6)
                w.bits(x >> tr, sig)
        pdelta = delta
        pt, pv = t, v
    return bytes(w.bytes)


def decode(data):
    r = BitReader(data)
    n = r.bits(16)
    t = r.bits(64)
    if t >= 1 << 63:
        t -= 1 << 64
    vb = r.bits(64)
    out = [(t, bitsf(vb))]
    delta = 0
    lead, trail = 0, 0
    for _ in range(n - 1):
        if r.bit() == 0:
            dod = 0
        else:
            nb = 0
            for prefix, size in BUCKETS:
                if r.bit() == 0:
                    nb = size
                    break
            if nb == 0:
                dod = r.bits(64)
                if dod >= 1 << 63:
                    dod -= 1 << 64
            else:
                dod = r.bits(nb)
                if dod > 1 << (nb - 1):
                    dod -= 1 << nb
        delta += dod
        t += delta
        if r.bit() == 1:
            if r.bit() == 1:
                lead = r.bits(5)
                sig = r.bits(6)
                if sig == 0:
                    sig = 64
                trail = 64 - lead - sig
            x = r.bits(64 - lead - trail) << trail
            vb ^= x
        out.append((t, bitsf(vb)))
    return out


# ------------------------------------------------------------ the database

class Db:
    def __init__(self):
        self.series = {}  # display key -> (labels, samples)
        self.out = []

    def ingest(self, name, parsed):
        added = 0
        dups = 0
        rejects = []
        touched = set()
        for no, sample, err in parsed:
            if err is not None:
                rejects.append(f"  ! line {no}: {err}")
                continue
            labels, v, t = sample
            key = show(labels)
            s = self.series.get(key)
            if s is None:
                s = (labels, [])
                self.series[key] = s
            samples = s[1]
            if samples and t < samples[-1][0]:
                rejects.append(f"  ! line {no}: out of order sample for {key} at {t}")
                continue
            if samples and t == samples[-1][0]:
                if v == samples[-1][1]:
                    dups += 1
                else:
                    rejects.append(f"  ! line {no}: {key} already has a different value at {t}")
                continue
            samples.append((t, v))
            touched.add(key)
            added += 1
        line = f"{name}: {added} samples added to {len(touched)} series"
        if dups:
            line += f", {dups} duplicate ignored" if dups == 1 else f", {dups} duplicates ignored"
        if rejects:
            line += f", {len(rejects)} rejected"
        self.out.append(line)
        self.out += rejects

    def write_block(self):
        os.makedirs(os.path.join("data", "run"), exist_ok=True)
        blob = bytearray()
        index = []
        total = 0
        nchunks = 0
        self.out.append("== block")
        for key in sorted(self.series):
            samples = self.series[key][1]
            if not samples:
                continue
            start = len(blob)
            chunks = []
            for i in range(0, len(samples), CHUNK):
                part = samples[i:i + CHUNK]
                c = encode(part)
                chunks.append(f"chunk {len(blob)} {len(c)} {part[0][0]} {part[-1][0]} {len(part)}")
                blob += c
            index.append(f"series {key} {len(chunks)}")
            index += chunks
            total += len(samples)
            nchunks += len(chunks)
            self.out.append(f"{key}: {len(samples)} samples in {len(chunks)} "
                            f"chunk{'s' if len(chunks) != 1 else ''}, {len(blob) - start} bytes")
        with open(os.path.join("data", "run", "chunks"), "wb") as fh:
            fh.write(blob)
        with open(os.path.join("data", "run", "index"), "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(index) + "\n")
        self.out.append(f"{len(index) - nchunks} series, {total} samples, {nchunks} chunks, {len(blob)} bytes, "
                        f"{len(blob) / total:.2f} bytes a sample")


def load_block():
    with open(os.path.join("data", "run", "chunks"), "rb") as fh:
        blob = fh.read()
    with open(os.path.join("data", "run", "index"), encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    series = []
    for l in lines:
        w = l.split(" ")
        if w[0] == "series":
            series.append([w[1], []])
        elif w[0] == "chunk":
            off, n = int(w[1]), int(w[2])
            got = decode(blob[off:off + n])
            if len(got) != int(w[5]) or got[0][0] != int(w[3]) or got[-1][0] != int(w[4]):
                raise Fail(f"chunk at {off} does not match the index")
            series[-1][1] += got
    return series


def labels_of(key):
    labels = {}
    i = key.find("{")
    name = key if i < 0 else key[:i]
    if name:
        labels["__name__"] = name
    if i >= 0:
        body = key[i + 1:-1]
        for part in body.split('",'):
            if not part:
                continue
            k, v = part.split('="', 1)
            labels[k] = v.rstrip('"')
    return labels


# ------------------------------------------------------------ queries

AGGS = ("sum", "avg", "max", "min", "count")
FUNCS = ("rate", "increase", "avg_over_time", "max_over_time", "min_over_time", "count_over_time")


def tokenize(src):
    toks = []
    i = 0
    while i < len(src):
        c = src[i]
        if c == " ":
            i += 1
            continue
        col = i + 1
        if is_name_start(c):
            j = i
            while j < len(src) and is_name_char(src[j]):
                j += 1
            toks.append(("name", src[i:j], col))
            i = j
        elif "0" <= c <= "9":
            j = i
            while j < len(src) and (src[j].isascii() and (src[j].isalnum() or src[j] == ".")):
                j += 1
            toks.append(("num", src[i:j], col))
            i = j
        elif c == '"':
            j = src.find('"', i + 1)
            if j < 0:
                raise Fail(f"parse error at column {col}: a string is not closed")
            toks.append(("str", src[i + 1:j], col))
            i = j + 1
        elif src.startswith("!=", i):
            toks.append(("op", "!=", col))
            i += 2
        elif c in "(){}[],=*/":
            toks.append(("op", c, col))
            i += 1
        else:
            raise Fail(f"parse error at column {col}: unexpected {c}")
    toks.append(("end", "", len(src) + 1))
    return toks


def duration_ms(s):
    units = {"s": 1000, "m": 60000, "h": 3600000}
    if len(s) < 2 or s[-1] not in units or not is_digits(s[:-1]):
        return None
    return int(s[:-1]) * units[s[-1]]


class Parser:
    def __init__(self, src):
        self.toks = tokenize(src)
        self.i = 0

    def peek(self):
        return self.toks[self.i]

    def take(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, value):
        t = self.take()
        if t[0] == "end" or t[1] != value or t[0] == "str":
            raise Fail(f"parse error at column {t[2]}: expected {value}")
        return t

    def parse(self):
        e = self.expr()
        t = self.peek()
        if t[0] != "end":
            raise Fail(f"parse error at column {t[2]}: unexpected {t[1]}")
        return e

    def expr(self):
        e = self.unary()
        while self.peek()[0] == "op" and self.peek()[1] in "*/":
            op = self.take()[1]
            t = self.take()
            if t[0] != "num" or not is_number(t[1]):
                raise Fail(f"parse error at column {t[2]}: expected a number")
            e = ("scalar", op, float(t[1]), e)
        return e

    def unary(self):
        t = self.take()
        if t[0] != "name":
            raise Fail(f"parse error at column {t[2]}: expected a metric, function or aggregation")
        if t[1] in AGGS and self.peek()[1] in ("by", "("):
            by = None
            if self.peek()[1] == "by" and self.peek()[0] == "name":
                self.take()
                self.expect("(")
                by = []
                while True:
                    n = self.take()
                    if n[0] != "name":
                        raise Fail(f"parse error at column {n[2]}: expected a label name")
                    by.append(n[1])
                    if self.peek()[1] == ",":
                        self.take()
                        continue
                    self.expect(")")
                    break
            self.expect("(")
            inner = self.expr()
            self.expect(")")
            return ("agg", t[1], by, inner)
        if t[1] in FUNCS and self.peek()[1] == "(":
            self.take()
            inner = self.expr()
            self.expect(")")
            return ("func", t[1], inner)
        matchers = [("__name__", "=", t[1])]
        if self.peek()[1] == "{" and self.peek()[0] == "op":
            self.take()
            while self.peek()[1] != "}":
                n = self.take()
                if n[0] != "name":
                    raise Fail(f"parse error at column {n[2]}: expected a label name")
                op = self.take()
                if op[0] != "op" or op[1] not in ("=", "!="):
                    raise Fail(f"parse error at column {op[2]}: expected = or !=")
                v = self.take()
                if v[0] != "str":
                    raise Fail(f"parse error at column {v[2]}: expected a quoted value")
                matchers.append((n[1], op[1], v[1]))
                if self.peek()[1] == ",":
                    self.take()
                elif self.peek()[1] != "}":
                    t2 = self.peek()
                    raise Fail(f"parse error at column {t2[2]}: expected , or }}")
            self.take()
        if self.peek()[1] == "[" and self.peek()[0] == "op":
            self.take()
            d = self.take()
            ms = duration_ms(d[1]) if d[0] == "num" else None
            if ms is None:
                raise Fail(f"parse error at column {d[2]}: expected a duration like 5m")
            self.expect("]")
            return ("range", matchers, ms)
        return ("select", matchers)


class Engine:
    def __init__(self, series):
        self.series = [(labels_of(k), s) for k, s in series]

    def matching(self, matchers):
        for labels, samples in self.series:
            if all((labels.get(k, "") == v) == (op == "=") for k, op, v in matchers):
                yield labels, samples

    def eval(self, e, t):
        kind = e[0]
        if kind == "select":
            out = []
            for labels, samples in self.matching(e[1]):
                last = None
                for ts, v in samples:
                    if t - LOOKBACK < ts <= t:
                        last = v
                if last is not None:
                    out.append((dict(labels), last))
            return out
        if kind == "range":
            raise Fail("a range vector needs a function such as rate around it")
        if kind == "scalar":
            out = []
            for labels, v in self.eval(e[3], t):
                labels.pop("__name__", None)
                out.append((labels, v * e[2] if e[1] == "*" else v / e[2]))
            return out
        if kind == "func":
            arg = e[2]
            if arg[0] != "range":
                raise Fail(f"{e[1]} takes a range vector, like {e[1]}(x[5m])")
            out = []
            for labels, samples in self.matching(arg[1]):
                win = [(ts, v) for ts, v in samples if t - arg[2] < ts <= t]
                r = func(e[1], win, t - arg[2], t, arg[2])
                if r is not None:
                    l = dict(labels)
                    l.pop("__name__", None)
                    out.append((l, r))
            return out
        _, op, by, inner = e
        groups = {}
        order = []
        for labels, v in sorted(self.eval(inner, t), key=lambda x: show(x[0])):
            g = {k: labels[k] for k in (by or []) if k in labels}
            key = show(g)
            if key not in groups:
                groups[key] = (g, [])
                order.append(key)
            groups[key][1].append(v)
        out = []
        for key in order:
            g, vs = groups[key]
            if op == "sum":
                r = 0.0
                for v in vs:
                    r += v
            elif op == "avg":
                r = 0.0
                for v in vs:
                    r += v
                r = r / len(vs)
            elif op == "max":
                r = vs[0]
                for v in vs[1:]:
                    if v > r:
                        r = v
            elif op == "min":
                r = vs[0]
                for v in vs[1:]:
                    if v < r:
                        r = v
            else:
                r = float(len(vs))
            out.append((g, r))
        return out


def func(name, win, start, end, rng):
    if name == "count_over_time":
        return float(len(win)) if win else None
    if not win:
        return None
    if name == "avg_over_time":
        s = 0.0
        for _, v in win:
            s += v
        return s / len(win)
    if name == "max_over_time":
        r = win[0][1]
        for _, v in win[1:]:
            if v > r:
                r = v
        return r
    if name == "min_over_time":
        r = win[0][1]
        for _, v in win[1:]:
            if v < r:
                r = v
        return r
    if len(win) < 2:
        return None
    first, last = win[0], win[-1]
    result = last[1] - first[1]
    prev = first[1]
    for _, v in win[1:]:
        if v < prev:
            result += prev
        prev = v
    dur_start = (first[0] - start) / 1000.0
    dur_end = (end - last[0]) / 1000.0
    sampled = (last[0] - first[0]) / 1000.0
    avg_dur = sampled / (len(win) - 1)
    if result > 0 and first[1] >= 0:
        dur_zero = sampled * (first[1] / result)
        if dur_zero < dur_start:
            dur_start = dur_zero
    threshold = avg_dur * 1.1
    extrap = sampled
    extrap += dur_start if dur_start < threshold else avg_dur / 2
    extrap += dur_end if dur_end < threshold else avg_dur / 2
    result = result * (extrap / sampled)
    if name == "rate":
        result = result / (rng / 1000.0)
    return result


def run_query(engine, line):
    w = line.split(" ")
    out = [f"> {line}"]
    try:
        if w[0] == "instant" and len(w) >= 3 and is_digits(w[1]):
            e = Parser(" ".join(w[2:])).parse()
            res = engine.eval(e, T0 + int(w[1]) * 1000)
            rows = sorted((show(l), v) for l, v in res)
            out += [f"  {k} {fmt(v)}" for k, v in rows] or ["  (no data)"]
        elif w[0] == "range" and len(w) >= 5 and all(is_digits(x) for x in w[1:4]):
            start, end, step = int(w[1]), int(w[2]), int(w[3])
            if end < start or step == 0:
                raise Fail("a range needs start <= end and a step above 0")
            e = Parser(" ".join(w[4:])).parse()
            rows = {}
            t = start
            while t <= end:
                for l, v in engine.eval(e, T0 + t * 1000):
                    rows.setdefault(show(l), []).append(f"{t}={fmt(v)}")
                t += step
            out += [f"  {k} {' '.join(rows[k])}" for k in sorted(rows)] or ["  (no data)"]
        else:
            raise Fail("a query is: instant <t> <expr>, or range <start> <end> <step> <expr>")
    except Fail as e:
        out.append(f"  ! {e}")
    return out


def main():
    names = sorted(n for n in os.listdir("data") if n.endswith(".prom"))
    db = Db()
    db.out.append("== ingest")
    for name in names:
        with open(os.path.join("data", name), encoding="utf-8") as fh:
            db.ingest(name, parse_file(fh.read()))
    db.write_block()
    series = load_block()
    for key, samples in series:
        if samples != db.series[key][1]:
            raise SystemExit(f"{key} decodes differently")
    db.out.append("every chunk decodes back to its samples")
    engine = Engine(series)
    db.out.append("== queries")
    with open(os.path.join("data", "queries.promql"), encoding="utf-8") as fh:
        for line in fh.read().split("\n"):
            if line and not line.startswith("#"):
                db.out += run_query(engine, line)
    print("\n".join(db.out))


main()
