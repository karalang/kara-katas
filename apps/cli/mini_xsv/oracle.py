"""The oracle for mini_xsv: a Python mirror of the xsv 0.13.0 commands the
Kara port implements, written from xsv's source (and from the source of
the crates it calls: csv, streaming-stats and tabwriter), not from its
documentation. It reads data/jobs.txt, runs each job and prints the same
transcript mini_xsv.kara prints.

Where xsv's own output is unspecified (frequency ties come out in hash map
order, and parallel stats merge chunks in completion order), the port and
this mirror pick one order: ties by value, chunks in file order.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def emit(s):
    OUT.append(s)


class Fail(Exception):
    pass


# ------------------------------------------------------------ numbers

INT_RE = re.compile(r"[+-]?[0-9]+\Z")
FLOAT_RE = re.compile(r"[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?\Z")
I64_MIN, I64_MAX = -(1 << 63), (1 << 63) - 1


def parse_i64(s):
    """Rust's i64::from_str: a sign and digits, in range; no spaces."""
    if not INT_RE.match(s):
        return None
    v = int(s)
    if v < I64_MIN or v > I64_MAX:
        return None
    return v


def parse_f64(s):
    """Rust's f64::from_str for finite decimal text; no spaces."""
    if not FLOAT_RE.match(s):
        return None
    return float(s)


def fmt_f64(x):
    """Rust's Display for f64: the shortest digits that read back, never
    an exponent, and no '.0' on a whole number."""
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    r = repr(x)
    neg = r.startswith("-")
    if neg:
        r = r[1:]
    exp = 0
    if "e" in r:
        r, e = r.split("e")
        exp = int(e)
    if "." in r:
        ip, fp = r.split(".")
    else:
        ip, fp = r, ""
    digits = ip + fp
    point = len(ip) + exp
    if point <= 0:
        s = "0." + "0" * (-point) + digits
    elif point >= len(digits):
        s = digits + "0" * (point - len(digits))
    else:
        s = digits[:point] + "." + digits[point:]
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    s = s.lstrip("0") or "0"
    if s.startswith("."):
        s = "0" + s
    return ("-" if neg else "") + s


def to_i64_sat(x):
    if math.isnan(x):
        return 0
    if x >= 9.223372036854775807e18:
        return I64_MAX
    if x <= -9.223372036854775808e18:
        return I64_MIN
    return int(x)


# ------------------------------------------------------------ CSV reader

def parse_csv(text, delim):
    """csv-core's reader: quoting on, doubled quotes, any of CR, LF or CRLF
    ends a record, empty lines skipped. Returns (fields, byte, line) per
    record, where byte and line say where the read of that record began."""
    b = text.encode("utf-8")
    d = ord(delim)
    out = []
    i, n = 0, len(b)
    while i < n:
        start = i
        # skip empty lines
        while i < n and b[i] in (10, 13):
            i += 1
        if i >= n:
            break
        fields = []
        cur = bytearray()
        state = "start"
        while True:
            if i >= n:
                fields.append(bytes(cur))
                break
            c = b[i]
            i += 1
            if state == "start":
                if c == 34:
                    state = "quoted"
                elif c == d:
                    fields.append(bytes(cur))
                    cur = bytearray()
                elif c in (10, 13):
                    fields.append(bytes(cur))
                    break
                else:
                    cur.append(c)
                    state = "field"
            elif state == "field":
                if c == d:
                    fields.append(bytes(cur))
                    cur = bytearray()
                    state = "start"
                elif c in (10, 13):
                    fields.append(bytes(cur))
                    break
                else:
                    cur.append(c)
            elif state == "quoted":
                if c == 34:
                    state = "endquote"
                else:
                    cur.append(c)
            else:  # endquote
                if c == 34:
                    cur.append(34)
                    state = "quoted"
                elif c == d:
                    fields.append(bytes(cur))
                    cur = bytearray()
                    state = "start"
                elif c in (10, 13):
                    fields.append(bytes(cur))
                    break
                else:
                    cur.append(c)
                    state = "field"
        line = 1 + b[:start].count(b"\n")
        out.append(([f.decode("utf-8") for f in fields], start, line))
    return out


class Reader:
    """A file read the way csv::Reader reads it: `headers` is the first
    record, `items` the records after it (all of them with no_headers),
    each a list of fields or, past a record of the wrong length when the
    reader is not flexible, the error message string."""

    def __init__(self, path, delim=None, no_headers=False, flexible=False):
        if delim is None:
            delim = "\t" if path.endswith(".tsv") else ","
        with open(os.path.join(HERE, path), encoding="utf-8", newline="") as f:
            text = f.read()
        raw = parse_csv(text, delim)
        self.headers = raw[0][0] if raw else []
        items = []
        expected = None
        for k, (fields, byte, line) in enumerate(raw):
            if not flexible:
                if expected is None:
                    expected = len(fields)
                elif len(fields) != expected:
                    items.append(
                        "CSV error: record %d (line: %d, byte: %d): found record "
                        "with %d fields, but the previous record has %d fields"
                        % (k, line, byte, len(fields), expected))
                    continue
            items.append(fields)
        self.items = items if no_headers else items[1:]


def ok(item):
    if isinstance(item, str):
        raise Fail(item)
    return item


# ------------------------------------------------------------ CSV writer

class Writer:
    def __init__(self, delim=",", term="\n", quote='"', always=False,
                 escape=None):
        self.delim, self.term, self.quote = delim, term, quote
        self.always, self.escape = always, escape
        req = {delim, quote}
        if escape is not None:
            req.add(escape)
        if term in ("\n", "\r\n"):
            req |= {"\r", "\n"}
        else:
            req.add(term)
        self.req = req
        self.expected = None
        self.buf = []

    def field(self, f):
        if self.always or any(c in self.req for c in f):
            if self.escape is None:
                body = f.replace(self.quote, self.quote * 2)
            else:
                body = f.replace(self.quote, self.escape + self.quote)
            return self.quote + body + self.quote
        return f

    def write(self, rec):
        text = self.delim.join(self.field(f) for f in rec)
        self.buf.append(text)
        if self.expected is None:
            self.expected = len(rec)
        elif self.expected != len(rec):
            raise Fail("CSV error: found record with %d fields, but the "
                       "previous record has %d fields" % (len(rec), self.expected))
        if text == "":
            self.buf.append(self.quote * 2)
        self.buf.append(self.term)

    def text(self):
        return "".join(self.buf)


# ------------------------------------------------------------ tabwriter

def tabwrite(text, minwidth=2, padding=2):
    out = []
    lines = [[]]
    cur = []

    def flush():
        nonlocal lines, cur
        if cur:
            lines[-1].append("".join(cur))
            cur = []
        ws = [[] for _ in lines]
        for i, line in enumerate(lines):
            if not line:
                continue
            for col in range(len(ws[i]), len(line) - 1):
                width = minwidth
                count = 0
                for other in lines[i:]:
                    if col + 1 >= len(other):
                        break
                    count += 1
                    width = max(width, len(other[col]))
                for j in range(i, i + count):
                    ws[j].append(width)
        first = True
        for line, w in zip(lines, ws):
            if not first:
                out.append("\n")
            first = False
            for k, cell in enumerate(line):
                if k >= len(w):
                    out.append(cell)
                else:
                    out.append(cell + " " * (w[k] - len(cell) + padding))
        lines = [[]]

    for ch in text:
        if ch == "\t" or ch == "\n":
            lines[-1].append("".join(cur))
            cur = []
            if ch == "\n":
                ncells = len(lines[-1])
                lines.append([])
                if ncells == 1:
                    flush()
        else:
            cur.append(ch)
    flush()
    return "".join(out)


def condense(s, n):
    if n is None or n >= len(s):
        return s
    return s[:n] + "..."


# ------------------------------------------------------------ selections

def parse_selection(s):
    invert = False
    if s.startswith("!"):
        invert, s = True, s[1:]
    chars = list(s)
    pos = 0

    def cur():
        return chars[pos] if pos < len(chars) else None

    def bump():
        nonlocal pos
        if pos < len(chars):
            pos += 1

    def end_of_field():
        return cur() is None or cur() in ",-"

    def end_of_selector():
        return cur() is None or cur() == ","

    def parse_one():
        if cur() == '"':
            bump()
            name = ""
            while True:
                c = cur()
                if c is None:
                    raise Fail('Unclosed quote, missing closing ".')
                if c == '"':
                    bump()
                    if cur() == '"':
                        bump()
                        name += '""'
                        continue
                    break
                name += c
                bump()
        else:
            name = ""
            while not (end_of_field() or cur() == "["):
                name += cur()
                bump()
        if cur() == "[":
            bump()
            idx = ""
            while True:
                c = cur()
                if c is None:
                    raise Fail("Unclosed index bracket, missing closing ].")
                bump()
                if c == "]":
                    break
                idx += c
            if not re.match(r"[0-9]+\Z", idx):
                raise Fail("Could not convert '%s' to an integer: invalid digit found in string" % idx)
            return ("name", name, int(idx))
        if re.match(r"\+?[0-9]+\Z", name):
            return ("index", int(name))
        return ("name", name, 0)

    sels = []
    while cur() is not None:
        f1 = ("start",) if cur() == "-" else parse_one()
        f2 = None
        if cur() == "-":
            bump()
            f2 = ("end",) if end_of_selector() else parse_one()
        if not end_of_selector():
            raise Fail("Expected end of field but got '%s' instead." % cur())
        sels.append((f1, f2))
        bump()
    return (sels, invert)


def one_index(sel, first, use_names):
    kind = sel[0]
    if kind == "start":
        return 0
    if kind == "end":
        return 0 if len(first) == 0 else len(first) - 1
    if kind == "index":
        i = sel[1]
        if i < 1 or i > len(first):
            raise Fail("Selector index %d is out of bounds. Index must be >= 1 and <= %d." % (i, len(first)))
        return i - 1
    name, sidx = sel[1], sel[2]
    if not use_names:
        raise Fail("Cannot use names ('%s') in selection with --no-headers set." % name)
    found = 0
    for i, f in enumerate(first):
        if f == name:
            if found == sidx:
                return i
            found += 1
    if found == 0:
        raise Fail("Selector name '%s' does not exist as a named header in the given CSV data." % name)
    raise Fail("Selector index '%d' for name '%s' is out of bounds. Must be >= 0 and <= %d." % (sidx, name, found - 1))


def selection(spec, first, use_names):
    sels, invert = spec
    if not sels:
        return [] if invert else list(range(len(first)))
    idxs = []
    for f1, f2 in sels:
        if f2 is None:
            idxs.append(one_index(f1, first, use_names))
        else:
            a = one_index(f1, first, use_names)
            b = one_index(f2, first, use_names)
            if a <= b:
                idxs.extend(range(a, b + 1))
            else:
                idxs.extend(range(a, b - 1, -1))
    if invert:
        s = set(idxs)
        return [i for i in range(len(first)) if i not in s]
    return idxs


def normal(sel):
    return sorted(set(sel))


# ------------------------------------------------------------ arguments

SPECS = {
    "count": ("", "n"),
    "headers": ("", "j intersect"),
    "select": ("d", "n"),
    "slice": ("s e l i d", "n"),
    "search": ("s d", "i v n"),
    "sort": ("s d", "N R n"),
    "frequency": ("s l j d", "a no-nulls n"),
    "stats": ("s j d", "everything mode cardinality median nulls n"),
    "join": ("d", "left right full cross no-case nulls n"),
    "fixlengths": ("l d", ""),
    "flatten": ("c s d", "n"),
    "table": ("w p c d", ""),
    "fmt": ("t quote escape d", "crlf ascii quote-always"),
    "cat": ("d", "pad n"),
}
LONG = {"select": "s", "start": "s", "end": "e", "len": "l", "index": "i",
        "limit": "l", "jobs": "j", "length": "l", "condense": "c",
        "separator": "s", "width": "w", "pad": "p", "out-delimiter": "t",
        "delimiter": "d", "no-headers": "n", "ignore-case": "i",
        "invert-match": "v", "numeric": "N", "reverse": "R", "asc": "a",
        "just-names": "j"}


def parse_args(cmd, argv):
    vals, bools = SPECS[cmd]
    vals, bools = vals.split(), bools.split()
    opts, pos = {}, []
    k = 0
    while k < len(argv):
        a = argv[k]
        k += 1
        if a.startswith("-") and a != "-":
            name = a[2:] if a.startswith("--") else a[1:]
            if name not in vals and name not in bools and name in LONG:
                name = LONG[name]
            if cmd == "cat" and a == "-p":
                name = "pad"
            if name in vals:
                opts[name] = argv[k]
                k += 1
            elif name in bools:
                opts[name] = True
            else:
                raise Fail("Unknown flag: '%s'" % a)
        else:
            pos.append(a)
    return opts, pos


def delim_opt(v):
    if v is None:
        return None
    if v == "\\t":
        return "\t"
    return v


# ------------------------------------------------------------ commands

def cmd_count(o, p, w):
    r = Reader(p[0], delim_opt(o.get("d")), o.get("n", False))
    n = 0
    for it in r.items:
        ok(it)
        n += 1
    emit("%d\n" % n)


def cmd_headers(o, p, w):
    heads = []
    for path in p:
        r = Reader(path, delim_opt(o.get("d")))
        for h in r.headers:
            if not o.get("intersect") or h not in heads:
                heads.append(h)
    text = ""
    for i, h in enumerate(heads):
        if len(p) == 1 and not o.get("j"):
            text += "%d\t" % (i + 1)
        text += h + "\n"
    emit(text if o.get("j") else tabwrite(text))


def cmd_select(o, p, w):
    nh = o.get("n", False)
    spec = parse_selection(p[0])
    r = Reader(p[1], delim_opt(o.get("d")), nh)
    sel = selection(spec, r.headers, not nh)
    if not nh:
        w.write([r.headers[i] for i in sel])
    for it in r.items:
        rec = ok(it)
        w.write([rec[i] for i in sel])


def cmd_slice(o, p, w):
    nh = o.get("n", False)
    r = Reader(p[0], delim_opt(o.get("d")), nh)
    if not nh and r.headers:
        w.write(r.headers)
    g = lambda k: int(o[k]) if k in o else None
    s, e, l, i = g("s"), g("e"), g("l"), g("i")
    if i is not None:
        if s is not None or e is not None or l is not None:
            raise Fail("--index cannot be used with --start, --end or --len")
        start, end = i, i + 1
    elif e is not None and l is not None:
        raise Fail("--end and --len cannot be used at the same time.")
    elif e is None and l is None:
        start, end = s or 0, 1 << 62
    elif e is not None:
        start = s or 0
        if start > e:
            raise Fail("The end of the range (%d) must be greater than or\n"
                       "equal to the start of the range (%d)." % (e, start))
        end = e
    else:
        start = s or 0
        end = start + l
    items = r.items[start:]
    for it in items[:end - start]:
        w.write(ok(it))


def cmd_search(o, p, w):
    nh = o.get("n", False)
    pat = p[0]
    flags = re.IGNORECASE if o.get("i") else 0
    rx = re.compile(pat, flags)
    r = Reader(p[1], delim_opt(o.get("d")), nh)
    spec = parse_selection(o.get("s", ""))
    sel = selection(spec, r.headers, not nh)
    if not nh:
        w.write(r.headers)
    for it in r.items:
        rec = ok(it)
        m = any(rx.search(rec[i]) for i in sel)
        if o.get("v"):
            m = not m
        if m:
            w.write(rec)


def next_num(s):
    v = parse_i64(s)
    if v is not None:
        return ("i", v)
    f = parse_f64(s)
    if f is not None:
        return ("f", f)
    return None


def cmp_num(a, b):
    if a[0] == "i" and b[0] == "i":
        return (a[1] > b[1]) - (a[1] < b[1])
    x, y = float(a[1]), float(b[1])
    return (x > y) - (x < y)


def iter_cmp(a, b):
    for x, y in zip(a, b):
        x, y = x.encode(), y.encode()
        if x != y:
            return -1 if x < y else 1
    return (len(a) > len(b)) - (len(a) < len(b))


def iter_cmp_num(a, b):
    k = 0
    while True:
        x = next_num(a[k]) if k < len(a) else None
        y = next_num(b[k]) if k < len(b) else None
        k += 1
        if x is None and y is None:
            return 0
        if x is None:
            return -1
        if y is None:
            return 1
        c = cmp_num(x, y)
        if c != 0:
            return c


def cmd_sort(o, p, w):
    import functools
    nh = o.get("n", False)
    r = Reader(p[0], delim_opt(o.get("d")), nh)
    sel = selection(parse_selection(o.get("s", "")), r.headers, not nh)
    recs = [ok(it) for it in r.items]
    f = iter_cmp_num if o.get("N") else iter_cmp
    if o.get("R"):
        key = functools.cmp_to_key(lambda x, y: f([y[i] for i in sel], [x[i] for i in sel]))
    else:
        key = functools.cmp_to_key(lambda x, y: f([x[i] for i in sel], [y[i] for i in sel]))
    recs.sort(key=key)
    if not nh and r.headers:
        w.write(r.headers)
    for rec in recs:
        w.write(rec)


def chunks(n, jobs):
    """xsv's split of n indexed records over jobs: (start, len) pairs."""
    size = n if n < jobs else n // jobs
    if size == 0:
        return [(i, 0) for i in range(n)]
    count = n // size + (1 if n % size else 0)
    return [(i * size, min(size, n - i * size)) for i in range(count)]


def cmd_frequency(o, p, w):
    nh = o.get("n", False)
    r = Reader(p[0], delim_opt(o.get("d")), nh)
    sel = selection(parse_selection(o.get("s", "")), r.headers, not nh)
    heads = [r.headers[i] for i in sel]
    nsel = normal(sel)
    recs = [ok(it) for it in r.items]
    jobs = int(o.get("j", "1"))
    parts = chunks(len(recs), jobs) if jobs > 1 else [(0, len(recs))]
    if jobs > 1 and not recs:
        parts = []
    tabs = None
    for start, length in parts:
        part = [dict() for _ in nsel]
        for rec in recs[start:start + length]:
            for k, i in enumerate(nsel):
                if i >= len(rec):
                    continue
                v = rec[i].strip()
                if v or not o.get("no-nulls"):
                    part[k][v] = part[k].get(v, 0) + 1
        if tabs is None:
            tabs = part
        else:
            for t, q in zip(tabs, part):
                for v, c in q.items():
                    t[v] = t.get(v, 0) + c
    if tabs is None:
        tabs = []
    limit = int(o.get("l", "10"))
    w.write(["field", "value", "count"])
    for k, (h, tab) in enumerate(zip(heads, tabs)):
        if nh:
            h = str(k + 1)
        if o.get("a"):
            counts = sorted(tab.items(), key=lambda kv: (kv[1], kv[0].encode()))
        else:
            counts = sorted(tab.items(), key=lambda kv: (-kv[1], kv[0].encode()))
        if limit > 0:
            counts = counts[:limit]
        for v, c in counts:
            w.write([h, v if v else "(NULL)", str(c)])


# --- stats

NULL, UNICODE, FLOAT, INTEGER = "NULL", "Unicode", "Float", "Integer"


def sample_type(s):
    if s == "":
        return NULL
    if parse_i64(s) is not None:
        return INTEGER
    if parse_f64(s) is not None:
        return FLOAT
    return UNICODE


def merge_type(a, b):
    if a == b:
        return a
    if a == NULL:
        return b
    if b == NULL:
        return a
    if {a, b} == {FLOAT, INTEGER}:
        return FLOAT
    return UNICODE


class MinMax:
    def __init__(self):
        self.min = self.max = None

    def add(self, v):
        if self.min is None or v < self.min:
            self.min = v
        if self.max is None or v > self.max:
            self.max = v

    def merge(self, o):
        if self.min is None or (o.min is not None and o.min < self.min):
            self.min = o.min
        if self.max is None or (o.max is not None and o.max > self.max):
            self.max = o.max


class Online:
    def __init__(self):
        self.size, self.mean, self.var = 0, 0.0, 0.0

    def add(self, x):
        old = self.mean
        prevq = self.var * float(self.size)
        self.size += 1
        self.mean += (x - old) / float(self.size)
        self.var = (prevq + (x - old) * (x - self.mean)) / float(self.size)

    def merge(self, o):
        s1, s2 = float(self.size), float(o.size)
        md = (self.mean - o.mean) * (self.mean - o.mean)
        try:
            mean = ((s1 * self.mean) + (s2 * o.mean)) / (s1 + s2)
        except ZeroDivisionError:
            mean = math.nan
        try:
            var = (((s1 * self.var) + (s2 * o.var)) / (s1 + s2)) + \
                ((s1 * s2 * md) / ((s1 + s2) * (s1 + s2)))
        except ZeroDivisionError:
            var = math.nan
        self.size += o.size
        self.mean, self.var = mean, var


class Stats:
    def __init__(self, which):
        self.which = which
        self.typ = NULL
        self.sum_int, self.sum_float = 0, None
        self.strings, self.str_len = MinMax(), MinMax()
        self.ints, self.floats = MinMax(), MinMax()
        self.online = Online()
        self.mode = [] if (which["mode"] or which["cardinality"]) else None
        self.median = [] if which["median"] else None

    def add(self, s):
        st = sample_type(s)
        self.typ = merge_type(self.typ, st)
        t = self.typ
        # sum
        if s != "":
            if t == FLOAT:
                f = parse_f64(s)
                if self.sum_float is None:
                    self.sum_float = float(self.sum_int) + f
                else:
                    self.sum_float += f
            elif t == INTEGER:
                if self.sum_float is not None:
                    self.sum_float += parse_f64(s)
                else:
                    self.sum_int += parse_i64(s)
        # min/max
        self.str_len.add(len(s.encode()))
        if s != "":
            self.strings.add(s.encode())
            if t == FLOAT:
                n = parse_f64(s)
                self.floats.add(n)
                self.ints.add(to_i64_sat(n))
            elif t == INTEGER:
                n = parse_i64(s)
                self.ints.add(n)
                self.floats.add(float(n))
        if self.mode is not None:
            self.mode.append(s.encode())
        if t == NULL:
            if self.which["nulls"]:
                self.online.add(0.0)
        elif t in (FLOAT, INTEGER):
            if st == NULL:
                if self.which["nulls"]:
                    self.online.add(0.0)
            else:
                n = parse_f64(s)
                if self.median is not None:
                    self.median.append(n)
                self.online.add(n)

    def merge(self, o):
        self.typ = merge_type(self.typ, o.typ)
        if self.sum_float is not None and o.sum_float is not None:
            self.sum_float = self.sum_float + o.sum_float
        elif self.sum_float is not None:
            self.sum_float = self.sum_float + float(o.sum_int)
        elif o.sum_float is not None:
            self.sum_float = float(self.sum_int) + o.sum_float
        else:
            self.sum_int += o.sum_int
        self.strings.merge(o.strings)
        self.str_len.merge(o.str_len)
        self.ints.merge(o.ints)
        self.floats.merge(o.floats)
        self.online.merge(o.online)
        if self.mode is not None:
            self.mode.extend(o.mode)
        if self.median is not None:
            self.median.extend(o.median)

    def record(self):
        t = self.typ
        out = [t]
        if t == INTEGER:
            out.append(str(self.sum_int))
        elif t == FLOAT:
            out.append(fmt_f64(self.sum_float if self.sum_float is not None else 0.0))
        else:
            out.append("")
        if t == UNICODE and self.strings.min is not None:
            out += [self.strings.min.decode(), self.strings.max.decode()]
        elif t == INTEGER and self.ints.min is not None:
            out += [str(self.ints.min), str(self.ints.max)]
        elif t == FLOAT and self.floats.min is not None:
            out += [fmt_f64(self.floats.min), fmt_f64(self.floats.max)]
        else:
            out += ["", ""]
        if self.str_len.min is not None:
            out += [str(self.str_len.min), str(self.str_len.max)]
        else:
            out += ["", ""]
        if t in (FLOAT, INTEGER):
            v = self.online.var
            out += [fmt_f64(self.online.mean), fmt_f64(math.sqrt(v) if v >= 0 else math.nan)]
        else:
            out += ["", ""]
        if self.median is not None:
            data = sorted(self.median)
            n = len(data)
            if n == 0:
                out.append("")
            elif n == 1:
                out.append(fmt_f64(data[0]))
            elif n % 2 == 0:
                out.append(fmt_f64((data[n // 2 - 1] + data[n // 2]) / 2.0))
            else:
                out.append(fmt_f64(data[n // 2]))
        if self.mode is not None:
            data = sorted(self.mode)
            if self.which["mode"]:
                m = mode_on_sorted(data)
                out.append("N/A" if m is None else m.decode())
            if self.which["cardinality"]:
                out.append(str(len(set(data))))
        return out


def mode_on_sorted(data):
    mode = nxt = None
    mode_count = next_count = 0
    for x in data:
        if mode is not None and mode == x:
            mode_count += 1
        elif nxt is not None and nxt == x:
            next_count += 1
        else:
            nxt = x
            next_count = 0
        if next_count > mode_count:
            mode, mode_count = nxt, next_count
            nxt, next_count = None, 0
        elif next_count == mode_count:
            mode, mode_count = None, 0
    return mode


def cmd_stats(o, p, w):
    nh = o.get("n", False)
    r = Reader(p[0], delim_opt(o.get("d")), nh)
    sel = selection(parse_selection(o.get("s", "")), r.headers, not nh)
    heads = [r.headers[i] for i in sel]
    every = o.get("everything", False)
    which = {"nulls": o.get("nulls", False),
             "mode": o.get("mode", False) or every,
             "median": o.get("median", False) or every,
             "cardinality": o.get("cardinality", False) or every}
    recs = [ok(it) for it in r.items]
    jobs = int(o.get("j", "1"))
    parts = chunks(len(recs), jobs) if jobs > 1 and recs else [(0, len(recs))]
    total = None
    for start, length in parts:
        part = [Stats(which) for _ in sel]
        for rec in recs[start:start + length]:
            for k, i in enumerate(sel):
                part[k].add(rec[i])
        if total is None:
            total = part
        else:
            for a, b in zip(total, part):
                a.merge(b)
    fields = ["field", "type", "sum", "min", "max", "min_length",
              "max_length", "mean", "stddev"]
    if which["median"]:
        fields.append("median")
    if which["mode"]:
        fields.append("mode")
    if which["cardinality"]:
        fields.append("cardinality")
    w.write(fields)
    for k, (h, st) in enumerate(zip(heads, total)):
        w.write([str(k) if nh else h] + st.record())


# --- join

def join_key(rec, sel, casei):
    out = []
    for i in sel:
        v = rec[i].strip()
        if casei:
            v = "".join(c.lower()[0] for c in v)
        out.append(v)
    return tuple(out)


def cmd_join(o, p, w):
    picks = [o.get(k, False) for k in ("left", "right", "full", "cross")]
    if sum(picks) > 1:
        raise Fail("Please pick exactly one join operation.")
    nh = o.get("n", False)
    d = delim_opt(o.get("d"))
    r1 = Reader(p[1], d, nh)
    r2 = Reader(p[3], d, nh)
    sel1 = selection(parse_selection(p[0]), r1.headers, not nh)
    sel2 = selection(parse_selection(p[2]), r2.headers, not nh)
    if len(sel1) != len(sel2):
        raise Fail("Column selections must have the same number of columns, "
                   "but found column selections with %d and %d columns."
                   % (len(sel1), len(sel2)))
    casei, nulls = o.get("no-case", False), o.get("nulls", False)
    if not nh:
        w.write(r1.headers + r2.headers)
    right = o.get("right", False)
    if right:
        r1, r2, sel1, sel2 = r2, r1, sel2, sel1
    pad1, pad2 = [""] * len(r1.headers), [""] * len(r2.headers)
    if o.get("cross"):
        for it in r1.items:
            row1 = ok(it)
            for it2 in r2.items:
                w.write(row1 + ok(it2))
        return
    rows2 = []
    index = {}
    for it in r2.items:
        rec = ok(it)
        key = join_key(rec, sel2, casei)
        if nulls or not any(k == "" for k in key):
            index.setdefault(key, []).append(len(rows2))
        rows2.append(rec)
    written = [False] * len(rows2)
    full = o.get("full", False)
    outer = o.get("left", False) or right
    for it in r1.items:
        row1 = ok(it)
        key = join_key(row1, sel1, casei)
        hits = index.get(key)
        if hits is None:
            if right:
                w.write(pad2 + row1)
            elif outer or full:
                w.write(row1 + pad2)
            continue
        for k in hits:
            written[k] = True
            if right:
                w.write(rows2[k] + row1)
            else:
                w.write(row1 + rows2[k])
    if full:
        for k, done in enumerate(written):
            if not done:
                w.write(pad1 + rows2[k])


def cmd_fixlengths(o, p, w):
    d = delim_opt(o.get("d"))
    if "l" in o:
        length = int(o["l"])
        if length == 0:
            raise Fail("Length must be greater than 0.")
    else:
        length = 0
        for rec in Reader(p[0], d, True, True).items:
            nonempty = 0
            for k, f in enumerate(rec):
                if k == 0 or f != "":
                    nonempty = k + 1
            length = max(length, nonempty)
    for rec in Reader(p[0], d, True, True).items:
        if length >= len(rec):
            rec = rec + [""] * (length - len(rec))
        else:
            rec = rec[:length]
        w.write(rec)


def cmd_flatten(o, p, w):
    nh = o.get("n", False)
    r = Reader(p[0], delim_opt(o.get("d")), nh)
    sep = o.get("s", "#")
    n = int(o["c"]) if "c" in o else None
    text = ""
    first = True
    for it in r.items:
        if not first and sep != "":
            text += sep + "\n"
        first = False
        rec = ok(it)
        for k, (h, f) in enumerate(zip(r.headers, rec)):
            text += (str(k) if nh else h) + "\t" + condense(f, n) + "\n"
    emit(tabwrite(text))


def cmd_table(o, p, w):
    r = Reader(p[0], delim_opt(o.get("d")), True)
    n = int(o["c"]) if "c" in o else None
    tw = Writer("\t")
    for it in r.items:
        tw.write([condense(f, n) for f in ok(it)])
    emit(tabwrite(tw.text(), int(o.get("w", "2")), int(o.get("p", "2"))))


def cmd_fmt(o, p, w):
    r = Reader(p[0], delim_opt(o.get("d")), True)
    delim = delim_opt(o.get("t")) or ","
    term = "\r\n" if o.get("crlf") else "\n"
    if o.get("ascii"):
        delim, term = "\x1f", "\x1e"
    fw = Writer(delim, term, o.get("quote", '"'), o.get("quote-always", False),
                o.get("escape"))
    try:
        for it in r.items:
            fw.write(ok(it))
    finally:
        emit(fw.text())


def cmd_cat(o, p, w):
    mode, paths = p[0], p[1:]
    d = delim_opt(o.get("d"))
    if mode == "rows":
        nh = o.get("n", False)
        for k, path in enumerate(paths):
            r = Reader(path, d, nh)
            if k == 0 and not nh and r.headers:
                w.write(r.headers)
            for it in r.items:
                w.write(ok(it))
        return
    rdrs = [Reader(path, d, True) for path in paths]
    lengths = [len(r.headers) for r in rdrs]
    pos = [0] * len(rdrs)
    while True:
        rec = []
        done = 0
        stop = False
        for k, r in enumerate(rdrs):
            if pos[k] >= len(r.items):
                done += 1
                if o.get("pad"):
                    rec += [""] * lengths[k]
                else:
                    stop = True
                    break
            else:
                rec += ok(r.items[pos[k]])
                pos[k] += 1
        if stop or done >= len(rdrs):
            break
        w.write(rec)


COMMANDS = {
    "count": cmd_count, "headers": cmd_headers, "select": cmd_select,
    "slice": cmd_slice, "search": cmd_search, "sort": cmd_sort,
    "frequency": cmd_frequency, "stats": cmd_stats, "join": cmd_join,
    "fixlengths": cmd_fixlengths, "flatten": cmd_flatten,
    "table": cmd_table, "fmt": cmd_fmt, "cat": cmd_cat,
}

# Commands that write through a csv::Writer onto stdout; that writer is
# flushed when it drops, so what it holds is printed even on an error.
WRITES_CSV = {"select", "slice", "search", "sort", "frequency", "stats",
              "join", "fixlengths", "cat"}


def shown(a):
    if a != "" and all(c.isascii() and (c.isalnum() or c in "@%+=:,./-_") for c in a):
        return a
    return "'" + a.replace("'", "'\"'\"'") + "'"


def main():
    with open(os.path.join(HERE, "data", "jobs.txt"), encoding="utf-8") as f:
        jobs = [l for l in f.read().split("\n") if l]
    for line in jobs:
        argv = line.split("\t")
        emit("$ xsv " + " ".join(shown(a) for a in argv) + "\n")
        mark = len(OUT)
        cmd = argv[0]
        w = Writer()
        err = None
        try:
            opts, pos = parse_args(cmd, argv[1:])
            COMMANDS[cmd](opts, pos, w)
        except Fail as e:
            err = str(e)
        if cmd in WRITES_CSV:
            emit(w.text())
        out = "".join(OUT[mark:])
        if out and not out.endswith("\n"):
            emit("\n\\ no newline at end of output\n")
        if err is not None:
            for l in err.split("\n"):
                emit("! " + l + "\n")
            emit("[exit 1]\n")
    sys.stdout.write("".join(OUT))


main()
