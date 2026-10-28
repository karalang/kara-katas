"""The oracle for mini_mlr: a Python mirror of the Miller 6.13 behaviour the
jobs in data/jobs.txt reach, written from Miller's Go source (pkg/input,
pkg/output, pkg/mlrval, pkg/bifs, pkg/transformers, pkg/climain).

It reads data/ (written by mk.py) and prints the transcript mini_mlr.kara
must print: for each job `$ mlr <args>`, what mlr writes to stdout, then
each line it writes to stderr after `! `, then `[exit 1]` when it fails.

Run: python3 -I -B oracle.py > expected.out"""
import math
import os
import re
import sys
from functools import cmp_to_key

HERE = os.path.dirname(os.path.abspath(__file__))
I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1
OUT = []


def emit(s):
    OUT.append(s)


class Fail(Exception):
    """A run that stops: the text is what mlr wrote to stderr."""


# ================================================================ values
# A value keeps the text it was read with; arithmetic makes new text.
# Kinds: int, float, str, void, absent, err, map, arr.


class V:
    __slots__ = ("k", "s", "n")

    def __init__(self, k, s, n=None):
        self.k = k
        self.s = s
        self.n = n

    def copy(self):
        if self.k == "map":
            return V("map", "", [[k, v.copy()] for k, v in self.n])
        if self.k == "arr":
            return V("arr", "", [v.copy() for v in self.n])
        return self


VOID = V("void", "")
ABSENT = V("absent", "")
ERROR = V("err", "(error)")


def fmt_f64(x):
    """Go's strconv.FormatFloat(x, 'f', -1, 64): the shortest digits that
    read back, never an exponent."""
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "+Inf" if x > 0 else "-Inf"
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


def from_int(i):
    return V("int", str(i), i)


def from_float(f):
    return V("float", fmt_f64(f), f)


def from_string(s):
    return VOID if s == "" else V("str", s)


DEC = "0123456789"
OCT = "01234567"
HEX = "0123456789abcdefABCDEF"
FLOATCH = "0123456789.eE+-"
FLOAT_RE = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?\Z")


def scan_type(s):
    """pkg/scan/find.go: the shape of a field before it is parsed."""
    if s == "":
        return "str"
    i0 = s[0]
    if i0 in "+-":
        return scan_positive(s[1:])
    if i0 in DEC:
        return scan_positive(s)
    if i0 == ".":
        if len(s) == 1:
            return "str"
        return scan_dec_or_float(s)
    return "str"


def scan_dec_or_float(b):
    maybe_int = True
    for c in b:
        if c not in FLOATCH:
            return "str"
        if c not in DEC:
            maybe_int = False
    return "dec" if maybe_int else "float"


def scan_positive(b):
    if b == "":
        return "str"
    i0 = b[0]
    if i0 == ".":
        return "float" if all(c in FLOATCH for c in b) else "str"
    if i0 not in DEC:
        return "str"
    if len(b) == 1:
        return "dec"
    if i0 == "0":
        i1 = b[1]
        for (marks, digits, kind) in (("xX", HEX, "hex"), ("oO", OCT, "oct"), ("bB", "01", "bin")):
            if i1 in marks:
                if len(b) == 2:
                    return "str"
                return kind if all(c in digits for c in b[2:]) else "str"
        if all(c in DEC for c in b[1:]):
            return "str"          # a leading zero: 007, 08 (decimal or octal-looking)
    return scan_dec_or_float(b)


def infer(s):
    """mlrval.inferNormally: what a field read from a file is."""
    t = scan_type(s)
    if s == "":
        return VOID
    if t == "dec":
        i = int(s)
        if I64_MIN <= i <= I64_MAX:
            return V("int", s, i)
        return V("str", s)
    if t in ("hex", "oct", "bin"):
        neg = s[0] == "-"
        body = s[3:] if s[0] in "+-" else s[2:]
        base = {"hex": 16, "oct": 8, "bin": 2}[t]
        u = int(body, base)
        if t == "hex" and len(body) == 16 and "8" <= body[0] <= "f":
            if u >= 1 << 63:
                u -= 1 << 64
        elif u > I64_MAX:
            return V("str", s)
        return V("int", s, -u if neg else u)
    if t == "float":
        if not FLOAT_RE.match(s):
            return V("str", s)
        f = float(s)
        if math.isinf(f):
            return V("str", s)
        return V("float", s, f)
    return V("str", s)


def is_num(v):
    return v.k in ("int", "float")


def fl(v):
    return float(v.n)


# ---------------------------------------------------------------- arithmetic
# The dispositions of pkg/bifs/arithmetic.go for the kinds the jobs reach.


def plus(a, b):
    if a.k == "absent":
        return b if b.k != "void" else ABSENT
    if b.k == "absent":
        return a if a.k != "void" else ABSENT
    if a.k == "void":
        return b if is_num(b) or b.k == "void" else ERROR
    if b.k == "void":
        return a if is_num(a) else ERROR
    if not (is_num(a) and is_num(b)):
        return ERROR
    if a.k == "int" and b.k == "int":
        c = a.n + b.n
        if I64_MIN <= c <= I64_MAX:
            return from_int(c)
        return from_float(float(a.n) + float(b.n))
    return from_float(fl(a) + fl(b))


def negate(v):
    if v.k == "int":
        return from_int(-v.n)
    return from_float(-v.n)


def minus(a, b):
    if a.k == "absent":
        return b if b.k != "void" else ABSENT
    if b.k == "absent":
        return a if a.k != "void" else ABSENT
    if a.k == "void":
        if is_num(b):
            return negate(b)
        return VOID if b.k == "void" else ERROR
    if b.k == "void":
        return a if is_num(a) else ERROR
    if not (is_num(a) and is_num(b)):
        return ERROR
    if a.k == "int" and b.k == "int":
        c = a.n - b.n
        if I64_MIN <= c <= I64_MAX:
            return from_int(c)
        return from_float(float(a.n) - float(b.n))
    return from_float(fl(a) - fl(b))


def times(a, b):
    if a.k == "absent":
        return b if b.k != "void" else ABSENT
    if b.k == "absent":
        return a if a.k != "void" else ABSENT
    if a.k == "void":
        return b if is_num(b) or b.k == "void" else ERROR
    if b.k == "void":
        return a if is_num(a) else ERROR
    if not (is_num(a) and is_num(b)):
        return ERROR
    if a.k == "int" and b.k == "int":
        c = float(a.n) * float(b.n)
        if abs(c) > 9223372036854774784.0:
            return from_float(c)
        return from_int(a.n * b.n)
    return from_float(fl(a) * fl(b))


def divide(a, b):
    if a.k == "void" or b.k == "void":
        if a.k in ("int", "float", "void") and b.k in ("int", "float", "void"):
            return VOID
        return ERROR
    if b.k == "absent":
        return a
    if not (is_num(a) and is_num(b)):
        return ERROR
    if a.k == "int" and b.k == "int":
        if b.n == 0:
            return from_float(float(a.n) / float(b.n) if a.n else float("nan"))
        if a.n % b.n == 0:
            q = abs(a.n) // abs(b.n)
            return from_int(q if (a.n < 0) == (b.n < 0) else -q)
        return from_float(float(a.n) / float(b.n))
    return from_float(fl(a) / fl(b))


def bif_abs(v):
    if v.k == "int":
        return from_int(abs(v.n))
    if v.k == "float":
        return from_float(abs(v.n))
    return v


def bif_min(a, b):
    if a.k == "absent":
        return b
    if b.k == "absent":
        return a
    if is_num(a) and is_num(b):
        if a.k == "int" and b.k == "int":
            return a if a.n < b.n else b
        return from_float(min(fl(a), fl(b)))
    if is_num(a):
        return a
    if is_num(b):
        return b
    if a.k == "void" or b.k == "void":
        return VOID
    return a if a.s < b.s else b


def bif_max(a, b):
    if a.k == "absent":
        return b
    if b.k == "absent":
        return a
    if is_num(a) and is_num(b):
        if a.k == "int" and b.k == "int":
            return a if a.n > b.n else b
        return from_float(max(fl(a), fl(b)))
    if is_num(a):
        return b
    if is_num(b):
        return a
    if a.k == "void":
        return b
    if b.k == "void":
        return a
    return a if a.s > b.s else b


def collate_rank(v):
    if is_num(v):
        return 0
    if v.k in ("void", "str"):
        return 2
    return 3


def cmp(a, b):
    """mlrval collation (Cmp, LessThan, Equals, GreaterThan): numbers
    numerically, then empty and strings together by bytes."""
    ra, rb = collate_rank(a), collate_rank(b)
    if ra != rb:
        return -1 if ra < rb else 1
    if ra == 0:
        if a.k == "int" and b.k == "int":
            x, y = a.n, b.n
        else:
            x, y = fl(a), fl(b)
        return -1 if x < y else (1 if x > y else 0)
    if ra == 2:
        return -1 if a.s < b.s else (1 if a.s > b.s else 0)
    return 0


# ================================================================ records


class Rec:
    """An ordered record: [key, value] pairs, plus where it came from."""
    __slots__ = ("f", "fname", "fnum")

    def __init__(self, f=None, fname="(stdin)", fnum=0):
        self.f = f if f is not None else []
        self.fname = fname
        self.fnum = fnum

    def copy(self):
        return Rec([[k, v.copy()] for k, v in self.f], self.fname, self.fnum)

    def like(self, f):
        return Rec(f, self.fname, self.fnum)

    def index(self, k):
        for i, (kk, _) in enumerate(self.f):
            if kk == k:
                return i
        return -1

    def get(self, k):
        i = self.index(k)
        return None if i < 0 else self.f[i][1]

    def has(self, k):
        return self.index(k) >= 0

    def put(self, k, v):
        i = self.index(k)
        if i < 0:
            self.f.append([k, v])
        else:
            self.f[i][1] = v

    def prepend(self, k, v):
        i = self.index(k)
        if i < 0:
            self.f.insert(0, [k, v])
        else:
            self.f[i][1] = v

    def put_after(self, i, k, v):
        """PutReferenceAfter: insert after position i, returning the new
        position."""
        self.f.insert(i + 1, [k, v])
        return i + 1

    def remove(self, k):
        i = self.index(k)
        if i >= 0:
            del self.f[i]

    def keys(self):
        return [k for k, _ in self.f]

    def put_dedupe(self, k, v):
        if self.has(k):
            j = 2
            while self.has("%s_%d" % (k, j)):
                j += 1
            k = "%s_%d" % (k, j)
        self.f.append([k, v])


def selected(rec, names):
    """GetSelectedValuesAndJoined: the values, or None if one is missing."""
    vals = []
    for n in names:
        v = rec.get(n)
        if v is None:
            return None
        vals.append(v)
    return vals


def joined(vals):
    return ",".join(v.s for v in vals)


# ================================================================ regexes


def miller_regex(s):
    """lib.CompileMillerRegex: "..." and /.../ lose their delimiters, a
    trailing i makes it case-insensitive."""
    if len(s) >= 2:
        if len(s) >= 3 and s[-1] == "i" and s[0] in "\"/" and s[-2] == s[0]:
            return re.compile("(?i)" + s[1:-2])
        if s[0] in "\"/" and s[-1] == s[0]:
            return re.compile(s[1:-1])
    return re.compile(s)


def sub_captures(name, rx, repl, gsub):
    """lib.RegexCompiledSub (first match, \\1..\\9) and ReplaceAllString."""
    if gsub:
        return rx.sub(lambda m: repl, name)
    m = rx.search(name)
    if not m:
        return name
    out = []
    i = 0
    while i < len(repl):
        c = repl[i]
        if c == "\\" and i + 1 < len(repl) and repl[i + 1] in "0123456789":
            g = int(repl[i + 1])
            out.append((m.group(g) or "") if g <= rx.groups else "")
            i += 2
        else:
            out.append(c)
            i += 1
    return name[:m.start()] + "".join(out) + name[m.end():]


# ================================================================ options

SEPARATORS = {
    "colon": ":", "comma": ",", "equals": "=", "newline": "\n", "pipe": "|",
    "semicolon": ";", "slash": "/", "space": " ", "tab": "\t", "lf": "\n",
}
DEFAULT_FS = {"csv": ",", "dkvp": ",", "nidx": " ", "markdown": " ", "pprint": " ",
              "tsv": "\t", "xtab": "\n", "json": ","}
DEFAULT_PS = {"dkvp": "=", "xtab": " "}


def sep(name):
    return SEPARATORS.get(name, name)


class Opts:
    def __init__(self):
        self.ifmt = "dkvp"
        self.ofmt = "dkvp"
        self.ifs = None
        self.ofs = None
        self.ips = None
        self.ops = None
        self.repifs = None
        self.implicit = False
        self.headerless = False
        self.ragged = False
        self.quote_all = False
        self.jlistwrap = True
        self.jvstack = True
        self.auto_unflatten = True
        self.xvright = False
        self.barred = False
        self.right = False
        self.files = []
        self.no_input = False


def flag_io(o, i=None, out=None):
    if i:
        o.ifmt = i
    if out:
        o.ofmt = out


MAIN_FLAGS0 = {
    "--icsv": lambda o: flag_io(o, "csv"),
    "--itsv": lambda o: flag_io(o, "tsv"),
    "--idkvp": lambda o: flag_io(o, "dkvp"),
    "--inidx": lambda o: flag_io(o, "nidx"),
    "--ocsv": lambda o: flag_io(o, None, "csv"),
    "--otsv": lambda o: flag_io(o, None, "tsv"),
    "--odkvp": lambda o: flag_io(o, None, "dkvp"),
    "--oxtab": lambda o: flag_io(o, None, "xtab"),
    "--opprint": lambda o: flag_io(o, None, "pprint"),
    "--omd": lambda o: flag_io(o, None, "markdown"),
    "--csv": lambda o: flag_io(o, "csv", "csv"),
    "--tsv": lambda o: flag_io(o, "tsv", "tsv"),
    "--c2t": lambda o: flag_io(o, "csv", "tsv"),
    "--c2d": lambda o: flag_io(o, "csv", "dkvp"),
    "--c2p": lambda o: flag_io(o, "csv", "pprint"),
    "--c2m": lambda o: flag_io(o, "csv", "markdown"),
    "--repifs": lambda o: setattr(o, "repifs", True),
    "--implicit-csv-header": lambda o: setattr(o, "implicit", True),
    "--hi": lambda o: setattr(o, "implicit", True),
    "--headerless-csv-output": lambda o: setattr(o, "headerless", True),
    "--ho": lambda o: setattr(o, "headerless", True),
    "--allow-ragged-csv-input": lambda o: setattr(o, "ragged", True),
    "--quote-all": lambda o: setattr(o, "quote_all", True),
    "--jvstack": lambda o: setattr(o, "jvstack", True),
    "--no-jvstack": lambda o: setattr(o, "jvstack", False),
    "--jlistwrap": lambda o: setattr(o, "jlistwrap", True),
    "--no-jlistwrap": lambda o: setattr(o, "jlistwrap", False),
    "--no-auto-unflatten": lambda o: setattr(o, "auto_unflatten", False),
    "--xvright": lambda o: setattr(o, "xvright", True),
    "--barred": lambda o: setattr(o, "barred", True),
    "--right": lambda o: setattr(o, "right", True),
    "-n": lambda o: setattr(o, "no_input", True),
}


def flag_ojson(o):
    o.ofmt = "json"
    o.jlistwrap = True
    o.jvstack = True


def flag_ojsonl(o):
    o.ofmt = "json"
    o.jlistwrap = False
    o.jvstack = False


def flag_onidx(o):
    o.ofmt = "nidx"
    o.ofs = " "


def flag_c2n(o):
    o.ifmt = "csv"
    flag_onidx(o)


def flag_c2j(o):
    o.ifmt = "csv"
    flag_ojson(o)


MAIN_FLAGS0.update({"--ojson": flag_ojson, "--ojsonl": flag_ojsonl, "--onidx": flag_onidx,
                    "--c2n": flag_c2n, "--c2j": flag_c2j})


def set_ifs(o, a):
    o.ifs = sep(a)


def set_ofs(o, a):
    o.ofs = sep(a)


def set_fs(o, a):
    o.ifs = sep(a)
    o.ofs = sep(a)


def set_ops(o, a):
    o.ops = sep(a)


MAIN_FLAGS1 = {
    "--ifs": set_ifs, "--ofs": set_ofs, "--fs": set_fs, "--ops": set_ops,
    "--from": lambda o, a: o.files.append(a),
}


def finalize(o):
    o.nidx_regex = False
    if o.repifs is None:
        if o.ifmt == "nidx" and o.ifs is None:
            o.nidx_regex = True
        o.repifs = o.ifmt == "pprint"
    if o.ifs is None:
        o.ifs = DEFAULT_FS[o.ifmt]
    if o.ips is None:
        o.ips = DEFAULT_PS.get(o.ifmt, "=")
    if o.ofs is None:
        o.ofs = DEFAULT_FS[o.ofmt]
    if o.ops is None:
        o.ops = DEFAULT_PS.get(o.ofmt, "=")


def getoptify(args):
    out = []
    for a in args:
        if re.match(r"^-[a-zA-Z0-9]+\Z", a) and not re.match(r"^-[0-9]+\Z", a):
            out.extend("-" + c for c in a[1:])
        elif re.match(r"^--[^=]+=.+\Z", a):
            out.extend(a.split("=", 1))
        else:
            out.append(a)
    return out


# ================================================================ readers


def read_text(path):
    with open(os.path.join(HERE, path), encoding="utf-8", newline="") as f:
        return f.read()


def lines_of(text):
    """The line reader: split on LF, drop a CR before it; a last line
    without LF still counts."""
    if text == "":
        return []
    parts = text.split("\n")
    if parts[-1] == "":
        parts.pop()
    return [p[:-1] if p.endswith("\r") else p for p in parts]


def csv_rows(text, comma):
    """encoding/csv as Miller's fork reads it: CRLF becomes LF everywhere,
    quoted fields may hold the separator, quotes and line ends, blank
    lines are skipped."""
    text = text.replace("\r\n", "\n")
    rows = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "\n":
            i += 1
            continue
        row = []
        while True:
            if i < n and text[i] == '"':
                i += 1
                buf = []
                while i < n:
                    c = text[i]
                    if c == '"':
                        if i + 1 < n and text[i + 1] == '"':
                            buf.append('"')
                            i += 2
                            continue
                        i += 1
                        break
                    buf.append(c)
                    i += 1
                row.append("".join(buf))
            else:
                j = i
                while j < n and text[j] != comma and text[j] != "\n":
                    j += 1
                row.append(text[i:j])
                i = j
            if i < n and text[i] == comma:
                i += 1
                continue
            if i < n and text[i] == "\n":
                i += 1
            break
        rows.append(row)
    return rows


def read_csv(path, text, o, fnum):
    if text.startswith("\ufeff"):
        text = text[1:]
    out = []
    header = None
    need_header = not o.implicit
    rownum = 0
    for row in csv_rows(text, o.ifs[0]):
        if need_header:
            header = row
            rownum += 1
            need_header = False
            continue
        rownum += 1
        if header is None:
            header = [str(i + 1) for i in range(len(row))]
        rec = Rec(fname=path, fnum=fnum)
        nh, nd = len(header), len(row)
        if nh == nd:
            for k, v in zip(header, row):
                rec.put_dedupe(k, infer(v))
        else:
            if not o.ragged:
                return out, ("mlr: CSV header/data length mismatch %d != %d at filename %s row %d.\n"
                             % (nh, nd, path, rownum))
            for i in range(min(nh, nd)):
                rec.put_dedupe(header[i], infer(row[i]))
            for i in range(nh, nd):
                rec.put_dedupe(str(i + 1), infer(row[i]))
        out.append(rec)
    return out, None


def tsv_decode(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i < len(s) - 1:
            d = s[i + 1]
            m = {"\\": "\\", "n": "\n", "r": "\r", "t": "\t"}.get(d)
            if m is not None:
                out.append(m)
                i += 2
                continue
        out.append(c)
        i += 1
    return "".join(out)


def split_fs(line, fs, repifs):
    if line == "":
        return []
    parts = line.split(fs)
    if repifs:
        parts = [p for p in parts if p != ""]
    return parts


def read_tsv(path, text, o, fnum):
    out = []
    header = None
    lineno = 0
    for line in lines_of(text):
        lineno += 1
        fields = split_fs(line, o.ifs, o.repifs)
        if header is None:
            header = fields
            continue
        if not o.ragged and len(header) != len(fields):
            return out, ("mlr: TSV header/data length mismatch %d != %d at filename %s line  %d.\n"
                         % (len(header), len(fields), path, lineno))
        rec = Rec(fname=path, fnum=fnum)
        nh, nd = len(header), len(fields)
        for i in range(min(nh, nd)):
            rec.put_dedupe(header[i], infer(tsv_decode(fields[i])))
        for i in range(nh, nd):
            rec.put_dedupe(str(i + 1), infer(tsv_decode(fields[i])))
        for i in range(nd, nh):
            rec.put(header[i], VOID)
        out.append(rec)
    return out, None


def read_dkvp(path, text, o, fnum):
    out = []
    for line in lines_of(text):
        rec = Rec(fname=path, fnum=fnum)
        for i, pair in enumerate(split_fs(line, o.ifs, o.repifs)):
            kv = pair.split(o.ips, 1)
            if len(kv) == 1 and kv[0] == "":
                continue
            if len(kv) == 1:
                rec.put_dedupe(str(i + 1), infer(kv[0]))
            else:
                rec.put_dedupe(kv[0], infer(kv[1]))
        out.append(rec)
    return out, None


def read_nidx(path, text, o, fnum):
    out = []
    for line in lines_of(text):
        if o.nidx_regex:
            vals = [] if line == "" else re.split(r"[ \t]+", line)
        else:
            vals = split_fs(line, o.ifs, o.repifs)
        out.append(Rec([[str(i + 1), infer(v)] for i, v in enumerate(vals)], path, fnum))
    return out, None


READERS = {"csv": read_csv, "tsv": read_tsv, "dkvp": read_dkvp, "nidx": read_nidx}


def read_inputs(files, o):
    """Every file's records in order. A file stops at its first error; the
    later files are still read, and the last error is the one reported."""
    recs = []
    err = None
    for i, path in enumerate(files):
        got, e = READERS[o.ifmt](path, read_text(path), o, i + 1)
        recs.extend(got)
        if e is not None:
            err = e
    return recs, err


# ================================================================ writers


def runes(s):
    return len(s)


def csv_quote(field, comma, quote_all):
    if not quote_all:
        if field == "":
            return field
        if not (field == "\\." or any(c in field for c in ("\n", "\r", '"', comma))):
            return field
    return '"' + field.replace('"', '""') + '"'


def write_csv(recs, o, tsv=False):
    out = []
    first_keys = None
    need_header = not o.headerless
    for rec in recs:
        keys = rec.keys()
        if first_keys is None:
            first_keys = keys
        if need_header:
            if tsv:
                out.append(o.ofs.join(tsv_encode(k) for k in keys) + "\n")
            else:
                out.append(o.ofs.join(csv_quote(k, o.ofs, o.quote_all) for k in keys) + "\n")
            need_header = False
        fields = []
        for i, (k, v) in enumerate(rec.f):
            if i < len(first_keys) and k != first_keys[i]:
                kind = "TSV" if tsv else "CSV"
                return "".join(out), ('mlr: %s schema change: first keys "%s"; current keys "%s"\n'
                                      % (kind, o.ofs.join(first_keys), o.ofs.join(keys)))
            fields.append(tsv_encode(v.s) if tsv else v.s)
        while len(fields) < len(first_keys):
            fields.append("")
        if tsv:
            out.append(o.ofs.join(fields) + "\n")
        else:
            out.append(o.ofs.join(csv_quote(f, o.ofs, o.quote_all) for f in fields) + "\n")
    return "".join(out), None


def tsv_encode(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")


def write_tsv(recs, o):
    return write_csv(recs, o, True)


def write_dkvp(recs, o):
    out = []
    for rec in recs:
        out.append(o.ofs.join(k + o.ops + v.s for k, v in rec.f) + "\n")
    return "".join(out), None


def write_nidx(recs, o):
    return "".join(o.ofs.join(v.s for _, v in rec.f) + "\n" for rec in recs), None


def write_markdown(recs, o):
    out = []
    last = ""
    nheaders = 0
    for rec in recs:
        cur = ",".join(rec.keys())
        if last != "" and cur != last:
            last = ""
            if nheaders > 0:
                out.append("\n")
        if last == "":
            out.append("|" + "".join(" " + k + " |" for k in rec.keys()) + "\n")
            out.append("|" + " --- |" * len(rec.f) + "\n")
            last = cur
            nheaders += 1
        out.append("|" + "".join(" " + v.s.replace("|", "\\|") + " |" for _, v in rec.f) + "\n")
    return "".join(out), None


def write_xtab(recs, o):
    out = []
    first = True
    for rec in recs:
        maxk = max([1] + [runes(k) for k in rec.keys()])
        maxv = max([0] + [runes(v.s) for _, v in rec.f])
        if not first:
            out.append(o.ofs)
        first = False
        for k, v in rec.f:
            pad = maxk - runes(k)
            if len(o.ops) == 1:
                gap = o.ops * (1 + pad)
            else:
                gap = o.ops
            val = v.s
            if o.xvright:
                val = " " * (maxv - runes(val)) + val
            out.append(k + gap + val + o.ofs)
    return "".join(out), None


def pprint_batch(batch, o, out):
    widths = {}
    maxnf = 0
    for rec in batch:
        maxnf = max(maxnf, len(rec.f))
        for k, v in rec.f:
            w = max(1, runes(v.s))
            if w > widths.get(k, 0):
                widths[k] = w
    if maxnf == 0:
        return False
    for k in widths:
        widths[k] = max(widths[k], runes(k))
    ofs = o.ofs

    def pad(text, k):
        return ofs * (widths[k] - runes(text))

    if o.barred:
        def bar(rec):
            return "+-" + "-+-".join("-" * widths[k] for k in rec.keys()) + "-+\n"

        for idx, rec in enumerate(batch):
            if idx == 0 and not o.headerless:
                out.append(bar(rec))
                cells = [(pad(k, k) + k) if o.right else (k + pad(k, k)) for k in rec.keys()]
                out.append("|" + ofs + (ofs + "|" + ofs).join(cells) + ofs + "|\n")
                out.append(bar(rec))
            cells = [(pad(v.s, k) + v.s) if o.right else (v.s + pad(v.s, k)) for k, v in rec.f]
            out.append("|" + ofs + (ofs + "|" + ofs).join(cells) + ofs + "|\n")
            if idx == len(batch) - 1:
                out.append(bar(rec))
        return True
    for idx, rec in enumerate(batch):
        rows = []
        if idx == 0 and not o.headerless:
            rows.append([(k, k) for k in rec.keys()])
        rows.append([(k, v.s if v.s != "" else "-") for k, v in rec.f])
        for row in rows:
            line = []
            for j, (k, s) in enumerate(row):
                last = j == len(row) - 1
                if o.right:
                    line.append(pad(s, k) + s + ("\n" if last else ofs))
                else:
                    line.append(s + ("\n" if last else pad(s, k) + ofs))
            out.append("".join(line))
    return True


def write_pprint(recs, o):
    out = []
    batch = []
    last = None
    for rec in recs:
        cur = ",".join(rec.keys())
        if last is None:
            batch.append(rec)
            last = cur
        elif cur != last:
            if pprint_batch(batch, o, out):
                out.append("\n")
            batch = [rec]
            last = cur
        else:
            batch.append(rec)
    if batch:
        pprint_batch(batch, o, out)
    return "".join(out), None


def json_string(s):
    out = ['"']
    for ch in s:
        b = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ch == '"':
            out.append('\\"')
        elif b < 0x20:
            out.append("\\u%04x" % b)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def json_value(v, multiline, depth):
    if v.k == "map":
        return json_map(v.n, multiline, depth)
    if v.k == "arr":
        items = v.n
        terminal = all(x.k not in ("map", "arr") for x in items)
        if terminal or not multiline:
            return "[" + ", ".join(json_value(x, False, depth + 1) for x in items) + "]"
        out = ["[\n"]
        for i, x in enumerate(items):
            out.append("  " * depth + json_value(x, multiline, depth + 1))
            out.append(",\n" if i < len(items) - 1 else "\n")
        out.append("  " * (depth - 1) + "]")
        return "".join(out)
    if v.k in ("int", "float"):
        return v.s
    if v.k == "void":
        return '""'
    return json_string(v.s)


def json_map(pairs, multiline, depth):
    if not multiline:
        return "{" + ", ".join(json_string(k) + ": " + json_value(v, False, depth + 1)
                               for k, v in pairs) + "}"
    if not pairs:
        return "{}"
    out = ["{\n"]
    for i, (k, v) in enumerate(pairs):
        out.append("  " * depth + json_string(k) + ": " + json_value(v, True, depth + 1))
        out.append(",\n" if i < len(pairs) - 1 else "\n")
    out.append("  " * (depth - 1) + "}")
    return "".join(out)


def write_json(recs, o):
    out = []
    if o.jlistwrap:
        for i, rec in enumerate(recs):
            out.append("[\n" if i == 0 else ",\n")
            out.append(json_map(rec.f, o.jvstack, 1))
        if recs:
            out.append("\n]\n")
    else:
        for rec in recs:
            out.append(json_map(rec.f, o.jvstack, 1) + "\n")
    return "".join(out), None


WRITERS = {"csv": write_csv, "tsv": write_tsv, "dkvp": write_dkvp, "nidx": write_nidx,
           "markdown": write_markdown, "xtab": write_xtab, "pprint": write_pprint,
           "json": write_json}


def unflatten_terminal(v):
    if v.k == "str" and v.s == "{}":
        return V("map", "", [])
    if v.k == "str" and v.s == "[]":
        return V("arr", "", [])
    return v


def arrayify(v):
    if v.k == "map":
        if not v.n:
            return v
        ok = True
        for i, pair in enumerate(v.n):
            if pair[0] != str(i + 1):
                ok = False
            pair[1] = arrayify(pair[1])
        if ok:
            return V("arr", "", [p[1] for p in v.n])
        return v
    if v.k == "arr":
        return V("arr", "", [arrayify(x) for x in v.n])
    return v


def unflatten(rec):
    """CopyUnflattened with separator ".": a.b keys nest, "{}" and "[]"
    become empty collections, maps keyed 1..n become arrays."""
    out = Rec([], rec.fname, rec.fnum)
    affected = []
    for k, v in rec.f:
        if "." in k:
            path = k.split(".")
            if path[0] not in affected:
                affected.append(path[0])
            cur = out.f
            for j, piece in enumerate(path):
                last = j == len(path) - 1
                found = None
                for pair in cur:
                    if pair[0] == piece:
                        found = pair
                        break
                if last:
                    if found is None:
                        cur.append([piece, unflatten_terminal(v)])
                    else:
                        found[1] = unflatten_terminal(v)
                else:
                    if found is None or found[1].k != "map":
                        nm = V("map", "", [])
                        if found is None:
                            cur.append([piece, nm])
                        else:
                            found[1] = nm
                        cur = nm.n
                    else:
                        cur = found[1].n
        else:
            out.put(k, unflatten_terminal(v))
    for base in affected:
        out.put(base, arrayify(out.get(base)))
    return out


# ================================================================ verbs
# Each verb parses its own arguments from argv at position i (the verb
# name) and returns (new position, transform). A transform takes the whole
# record stream and returns the stream it emits, in order: what Miller
# emits on each record comes first, what it emits at the end comes last.


def need_arg(verb, argv, i):
    if i >= len(argv):
        raise Fail("mlr %s: option \"%s\" missing argument(s).\n" % (verb, argv[i - 1]))
    return argv[i]


def str_list(verb, argv, i):
    a = need_arg(verb, argv, i)
    return [] if a == "" else a.split(",")


def int_arg(verb, argv, i):
    a = need_arg(verb, argv, i)
    try:
        if not re.match(r"^[+-]?\d+\Z", a):
            raise ValueError
        return int(a)
    except ValueError:
        raise Fail('mlr %s: could not scan flag "%s" argument "%s" as int.\n' % (verb, a, a))


def flags(argv, i):
    """Walk a verb's flags: yields (flag, position after it)."""
    i += 1
    while i < len(argv):
        opt = argv[i]
        if not opt.startswith("-") or opt == "--":
            break
        yield opt, i + 1


class FlagWalk:
    def __init__(self, verb, argv, i):
        self.verb = verb
        self.argv = argv
        self.i = i + 1

    def next(self):
        if self.i < len(self.argv) and self.argv[self.i].startswith("-") and self.argv[self.i] != "--":
            opt = self.argv[self.i]
            self.i += 1
            return opt
        return None

    def s(self):
        a = need_arg(self.verb, self.argv, self.i)
        self.i += 1
        return a

    def lst(self):
        a = self.s()
        return [] if a == "" else a.split(",")

    def int(self):
        v = int_arg(self.verb, self.argv, self.i)
        self.i += 1
        return v

    def positional(self):
        if self.i >= len(self.argv):
            raise Fail("mlr %s: positional argument missing.\n" % self.verb)
        a = self.argv[self.i]
        self.i += 1
        return a

    def bad(self, opt):
        raise Fail("mlr %s: option \"%s\" not recognized.\n" % (self.verb, opt))


# ---------------------------------------------------------------- cat, head, tail, tac


def v_cat(argv, i, o):
    w = FlagWalk("cat", argv, i)
    numbers = False
    name = "n"
    groups = None
    do_fname = do_fnum = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-n":
            numbers = True
        elif opt == "-N":
            numbers = True
            name = w.s()
        elif opt == "-g":
            groups = w.lst()
        elif opt == "--filename":
            do_fname = True
        elif opt == "--filenum":
            do_fnum = True
        else:
            w.bad(opt)

    def run(recs):
        counter = 0
        counts = {}
        for rec in recs:
            if numbers:
                vals = selected(rec, groups) if groups else None
                if groups is None or vals is None:
                    counter += 1
                    c = counter
                else:
                    key = joined(vals)
                    c = counts.get(key, 0) + 1
                    counts[key] = c
                rec.prepend(name, from_int(c))
            if do_fname:
                rec.prepend("filename", from_string(rec.fname))
            if do_fnum:
                rec.prepend("filenum", from_int(rec.fnum))
        return recs
    return w.i, run


def v_head(argv, i, o, tail=False):
    verb = "tail" if tail else "head"
    w = FlagWalk(verb, argv, i)
    n = 10
    groups = []
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-n":
            n = abs(w.int())
        elif opt == "-g":
            groups = w.lst()
        else:
            w.bad(opt)

    def run(recs):
        if not tail:
            out = []
            counts = {}
            for rec in recs:
                vals = selected(rec, groups)
                if vals is None:
                    continue
                key = joined(vals)
                c = counts.get(key, 0)
                if c < n:
                    out.append(rec)
                counts[key] = c + 1
            return out
        order = []
        keep = {}
        for rec in recs:
            vals = selected(rec, groups)
            if vals is None:
                continue
            key = joined(vals)
            if key not in keep:
                keep[key] = []
                order.append(key)
            keep[key].append(rec)
            if len(keep[key]) > n:
                keep[key].pop(0)
        return [r for key in order for r in keep[key]]
    return w.i, run


def v_tail(argv, i, o):
    return v_head(argv, i, o, tail=True)


def v_tac(argv, i, o):
    w = FlagWalk("tac", argv, i)
    opt = w.next()
    if opt is not None:
        w.bad(opt)
    return w.i, lambda recs: list(reversed(recs))


def group_lists(recs, keyfn):
    order = []
    lists = {}
    for rec in recs:
        key = keyfn(rec)
        if key is None:
            continue
        if key not in lists:
            lists[key] = []
            order.append(key)
        lists[key].append(rec)
    return order, lists


def v_group_by(argv, i, o):
    w = FlagWalk("group-by", argv, i)
    opt = w.next()
    if opt is not None:
        w.bad(opt)
    names = w.positional().split(",")

    def run(recs):
        def key(rec):
            vals = selected(rec, names)
            return None if vals is None else joined(vals)
        order, lists = group_lists(recs, key)
        return [r for k in order for r in lists[k]]
    return w.i, run


def v_group_like(argv, i, o):
    w = FlagWalk("group-like", argv, i)
    opt = w.next()
    if opt is not None:
        w.bad(opt)

    def run(recs):
        order, lists = group_lists(recs, lambda rec: ",".join(rec.keys()))
        return [r for k in order for r in lists[k]]
    return w.i, run


def v_regularize(argv, i, o):
    w = FlagWalk("regularize", argv, i)

    def run(recs):
        seen = {}
        out = []
        for rec in recs:
            keys = rec.keys()
            sk = ",".join(sorted(keys))
            if sk not in seen:
                seen[sk] = keys
                out.append(rec)
            else:
                out.append(rec.like([[k, rec.get(k)] for k in seen[sk]]))
        return out
    return w.i, run


def v_sort_within_records(argv, i, o):
    w = FlagWalk("sort-within-records", argv, i)
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt != "-r":
            w.bad(opt)

    def run(recs):
        for rec in recs:
            rec.f.sort(key=lambda p: p[0])
        return recs
    return w.i, run


# ---------------------------------------------------------------- cut, having-fields, template


def v_cut(argv, i, o):
    w = FlagWalk("cut", argv, i)
    names = []
    ordered = complement = regexes = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            names = w.lst()
        elif opt == "-o":
            ordered = True
        elif opt in ("-x", "--complement"):
            complement = True
        elif opt == "-r":
            regexes = True
        else:
            w.bad(opt)
    rxs = [miller_regex(n) for n in names] if regexes else None

    def run(recs):
        out = []
        for rec in recs:
            if regexes:
                rec.f = [p for p in rec.f
                         if any(rx.search(p[0]) for rx in rxs) != complement]
            elif complement:
                rec.f = [p for p in rec.f if p[0] not in names]
            elif ordered:
                rec.f = [[n, rec.get(n)] for n in names if rec.has(n)]
            else:
                rec.f = [p for p in rec.f if p[0] in names]
            out.append(rec)
        return out
    return w.i, run


def v_having_fields(argv, i, o):
    w = FlagWalk("having-fields", argv, i)
    mode = None
    arg = None
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt in ("--at-least", "--which-are", "--at-most", "--all-defined", "--any-defined"):
            mode, arg = opt, w.lst()
        elif opt in ("--all-matching", "--any-matching", "--none-matching"):
            mode, arg = opt, miller_regex(w.s())
        else:
            w.bad(opt)

    def keep(rec):
        keys = rec.keys()
        if mode == "--at-least":
            return all(rec.has(n) for n in arg)
        if mode == "--which-are":
            return len(keys) == len(arg) and all(rec.has(n) for n in arg)
        if mode == "--at-most":
            return all(k in arg for k in keys)
        if mode == "--all-matching":
            return len(keys) > 0 and all(arg.search(k) for k in keys)
        if mode == "--any-matching":
            return any(arg.search(k) for k in keys)
        return not any(arg.search(k) for k in keys)
    return w.i, lambda recs: [r for r in recs if keep(r)]


def v_template(argv, i, o):
    w = FlagWalk("template", argv, i)
    names = []
    fill = ""
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            names = w.lst()
        elif opt == "--fill-with":
            fill = w.s()
        else:
            w.bad(opt)
    fv = from_string(fill)

    def run(recs):
        return [rec.like([[n, rec.get(n) if rec.has(n) else fv] for n in names]) for rec in recs]
    return w.i, run


def v_unsparsify(argv, i, o):
    w = FlagWalk("unsparsify", argv, i)
    fill = ""
    names = None
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "--fill-with":
            fill = w.s()
        elif opt == "-f":
            names = (names or []) + w.lst()
        else:
            w.bad(opt)
    fv = from_string(fill)

    def run(recs):
        if names is not None:
            for rec in recs:
                for n in names:
                    if not rec.has(n):
                        rec.put(n, fv)
            return recs
        union = []
        seen = set()
        for rec in recs:
            for k in rec.keys():
                if k not in seen:
                    seen.add(k)
                    union.append(k)
        return [rec.like([[k, rec.get(k) if rec.has(k) else fv] for k in union]) for rec in recs]
    return w.i, run


def v_fill_down(argv, i, o):
    w = FlagWalk("fill-down", argv, i)
    names = None
    do_all = only_absent = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            names = w.lst()
        elif opt == "--all":
            do_all = True
        elif opt in ("-a", "--only-if-absent"):
            only_absent = True
        else:
            w.bad(opt)

    def run(recs):
        last = {}
        for rec in recs:
            fields = rec.keys() if do_all else names
            for n in fields:
                v = rec.get(n)
                present = v is not None if only_absent else (v is not None and v.k != "void")
                if present:
                    last[n] = v
                elif n in last:
                    rec.put(n, last[n])
        return recs
    return w.i, run


def v_fill_empty(argv, i, o):
    w = FlagWalk("fill-empty", argv, i)
    fill = "N/A"
    inferring = True
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-v":
            fill = w.s()
        elif opt == "-S":
            inferring = False
        else:
            w.bad(opt)
    fv = infer(fill) if inferring else from_string(fill)

    def run(recs):
        for rec in recs:
            for p in rec.f:
                if p[1].k == "void":
                    p[1] = fv
        return recs
    return w.i, run


# ---------------------------------------------------------------- grep, decimate, sec2gmt


def v_grep(argv, i, o):
    w = FlagWalk("grep", argv, i)
    invert = icase = values_only = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-v":
            invert = True
        elif opt == "-i":
            icase = True
        elif opt == "-a":
            values_only = True
        else:
            w.bad(opt)
    pattern = w.positional()
    try:
        rx = re.compile(("(?i)" if icase else "") + pattern)
    except re.error:
        raise Fail('mlr grep: couldn\'t compile regex "%s"\n' % pattern)

    def text(rec):
        if values_only:
            return ",".join(v.s for _, v in rec.f)
        return ",".join(k + "=" + v.s for k, v in rec.f)
    return w.i, lambda recs: [r for r in recs if (rx.search(text(r)) is not None) != invert]


def v_decimate(argv, i, o):
    w = FlagWalk("decimate", argv, i)
    n = 10
    at_start = at_end = False
    groups = []
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-n":
            n = w.int()
        elif opt == "-b":
            at_start = True
        elif opt == "-e":
            at_end = True
        elif opt == "-g":
            groups = w.lst()
        else:
            w.bad(opt)
    keep_rem = 0 if (at_start and not at_end) else n - 1

    def run(recs):
        out = []
        counts = {}
        for rec in recs:
            vals = selected(rec, groups)
            if vals is None:
                continue
            key = joined(vals)
            c = counts.get(key, 0)
            if c % n == keep_rem:
                out.append(rec)
            counts[key] = c + 1
        return out
    return w.i, run


def days_to_civil(z):
    """Howard Hinnant's civil_from_days: proleptic Gregorian."""
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + 3 if mp < 10 else mp - 9
    return (y + 1 if m <= 2 else y), m, d


def go_trunc(x):
    return int(x)  # Go's int64(float) truncates toward zero, as Python's int does


def sec2gmt(x, places):
    ip = go_trunc(x)
    frac = x - float(ip)
    if frac < 0:
        ip -= 1
        frac += 1.0
    ns = go_trunc(frac * 1e9)
    ip += ns // 1000000000
    ns %= 1000000000
    days, secs = divmod(ip, 86400)
    y, m, d = days_to_civil(days)
    s = "%04d-%02d-%02dT%02d:%02d:%02d" % (y, m, d, secs // 3600, secs // 60 % 60, secs % 60)
    if places > 0:
        s += ".%0*d" % (places, ns // 10 ** (9 - places))
    return s + "Z"


def v_sec2gmt(argv, i, o):
    w = FlagWalk("sec2gmt", argv, i)
    pre = 1.0
    places = 0
    while True:
        opt = w.next()
        if opt is None:
            break
        if re.match(r"^-[1-9]\Z", opt):
            places = int(opt[1:])
        elif opt == "--millis":
            pre = 1.0e3
        elif opt == "--micros":
            pre = 1.0e6
        elif opt == "--nanos":
            pre = 1.0e9
        else:
            w.bad(opt)
    names = w.positional().split(",")

    def run(recs):
        for rec in recs:
            for n in names:
                v = rec.get(n)
                if v is not None and is_num(v):
                    rec.put(n, from_string(sec2gmt(fl(v) / pre, places)))
        return recs
    return w.i, run


def v_seqgen(argv, i, o):
    w = FlagWalk("seqgen", argv, i)
    name = "i"
    start, stop, step = "1", "100", "1"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            name = w.s()
        elif opt == "--start":
            start = w.s()
        elif opt == "--stop":
            stop = w.s()
        elif opt == "--step":
            step = w.s()
        else:
            w.bad(opt)

    def build():
        a, b, c = infer(start), infer(stop), infer(step)
        for v, label, text in ((a, "start", start), (b, "stop", stop), (c, "step", step)):
            if not is_num(v):
                raise Fail('mlr seqgen: %s value should be number; got "%s"\n' % (label, text))
        if fl(c) > 0:
            done = lambda x: cmp(x, b) > 0
        elif fl(c) < 0:
            done = lambda x: cmp(x, b) < 0
        elif cmp(a, b) == 0:
            done = lambda x: cmp(x, b) == 0
        else:
            raise Fail("mlr seqgen: step must not be zero unless start == stop.\n")

        def run(recs):
            out = []
            x = a
            while not done(x):
                out.append(Rec([[name, x]], "seqgen", 1))
                x = plus(x, c)
            return out
        return run
    return w.i, ("construct", build)


# ---------------------------------------------------------------- sort, top


def v_sort(argv, i, o):
    w = FlagWalk("sort", argv, i)
    keys = []

    def add(kind):
        for n in w.lst():
            keys.append((n, kind))
    while True:
        opt = w.next()
        if opt is None:
            break
        nxt = argv[w.i] if w.i < len(argv) else ""
        if opt == "-f":
            add("lex")
        elif opt == "-c":
            if nxt == "-r":
                w.i += 1
                add("foldr")
            else:
                add("fold")
        elif opt == "-r":
            add("lexr")
        elif opt == "-nf":
            add("num")
        elif opt == "-nr":
            add("numr")
        elif opt == "-n":
            if nxt == "-f":
                w.i += 1
                add("num")
            elif nxt == "-r":
                w.i += 1
                add("numr")
            else:
                add("num")
        else:
            w.bad(opt)
    names = [n for n, _ in keys]

    def fold(v):
        return v.s.lower() if v.k == "str" else v.s

    def c3(x, y):
        return -1 if x < y else (1 if x > y else 0)

    def compare(ga, gb):
        for (_, kind), a, b in zip(keys, ga[0], gb[0]):
            if kind == "lex":
                c = c3(a.s, b.s)
            elif kind == "lexr":
                c = c3(b.s, a.s)
            elif kind == "fold":
                c = c3(fold(a), fold(b))
            elif kind == "foldr":
                c = c3(fold(b), fold(a))
            elif kind == "num":
                c = cmp(a, b)
            else:
                c = -cmp(a, b)
            if c != 0:
                return c
        return 0

    def run(recs):
        order = []
        groups = {}
        spill = []
        for rec in recs:
            vals = selected(rec, names)
            if vals is None:
                spill.append(rec)
                continue
            key = joined(vals)
            if key not in groups:
                groups[key] = (vals, [])
                order.append(key)
            groups[key][1].append(rec)
        gl = [groups[k] for k in order]
        gl.sort(key=cmp_to_key(compare))
        return [r for g in gl for r in g[1]] + spill
    return w.i, run


def bsearch_insert(arr, value, descending):
    """BsearchMlrvalArrayFor{Descending,Ascending}Insert."""
    size = len(arr)
    if size == 0:
        return 0
    if descending:
        gt = lambda a, b: cmp(a, b) > 0
        lt = lambda a, b: cmp(a, b) < 0
    else:
        gt = lambda a, b: cmp(a, b) < 0
        lt = lambda a, b: cmp(a, b) > 0
    ge = lambda a, b: not lt(a, b)
    lo, hi = 0, size - 1
    mid = (hi + lo) // 2
    if gt(value, arr[0]):
        return 0
    if lt(value, arr[hi]):
        return size
    while lo < hi:
        m = arr[mid]
        if cmp(value, m) == 0:
            return mid
        elif gt(value, m):
            hi = mid
        else:
            lo = mid
        newmid = (hi + lo) // 2
        if mid == newmid:
            if ge(value, arr[lo]):
                return lo
            elif ge(value, arr[hi]):
                return hi
            return hi + 1
        mid = newmid
    return lo


class TopKeeper:
    def __init__(self, cap, do_max):
        self.cap = cap
        self.do_max = do_max
        self.vals = []
        self.recs = []

    def add(self, v, rec):
        d = bsearch_insert(self.vals, v, self.do_max)
        if len(self.vals) < self.cap:
            self.vals.insert(d, v)
            self.recs.insert(d, rec)
        elif d < self.cap:
            self.vals.insert(d, v)
            self.recs.insert(d, rec)
            self.vals.pop()
            self.recs.pop()


def v_top(argv, i, o):
    w = FlagWalk("top", argv, i)
    n = 1
    fields = []
    groups = []
    do_max = True
    show_full = False
    out_name = "top_idx"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-n":
            n = w.int()
        elif opt == "-f":
            fields = w.lst()
        elif opt == "-g":
            groups = w.lst()
        elif opt == "--max":
            do_max = True
        elif opt == "--min":
            do_max = False
        elif opt == "-a":
            show_full = True
        elif opt == "-o":
            out_name = w.s()
        else:
            w.bad(opt)

    def run(recs):
        order = []
        table = {}
        for rec in recs:
            fv = selected(rec, fields)
            gv = selected(rec, groups)
            if fv is None or gv is None:
                continue
            key = joined(gv)
            if key not in table:
                table[key] = (gv, {})
                order.append(key)
            second = table[key][1]
            for f, v in zip(fields, fv):
                if f not in second:
                    second[f] = TopKeeper(n, do_max)
                second[f].add(v, rec.copy() if show_full else None)
        out = []
        for key in order:
            gv, second = table[key]
            if show_full:
                for f in fields:
                    if f in second:
                        out.extend(r.copy() for r in second[f].recs)
                continue
            for j in range(n):
                rec = Rec()
                for g, v in zip(groups, gv):
                    rec.put(g, v)
                for f in fields:
                    if f not in second:
                        continue
                    keeper = second[f]
                    rec.put(out_name, from_int(j + 1))
                    rec.put(f + "_top", keeper.vals[j] if j < len(keeper.vals) else VOID)
                out.append(rec)
        return out
    return w.i, run


# ---------------------------------------------------------------- counting


def v_count(argv, i, o):
    w = FlagWalk("count", argv, i)
    groups = None
    only_n = False
    name = "count"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-g":
            groups = w.lst()
        elif opt == "-n":
            only_n = True
        elif opt == "-o":
            name = w.s()
        else:
            w.bad(opt)

    def run(recs):
        if groups is None:
            return [Rec([[name, from_int(len(recs))]])]
        order = []
        counts = {}
        for rec in recs:
            vals = selected(rec, groups)
            if vals is None:
                continue
            key = joined(vals)
            if key not in counts:
                counts[key] = [vals, 0]
                order.append(key)
            counts[key][1] += 1
        if only_n:
            return [Rec([[name, from_int(len(order))]])]
        return [Rec([[g, v] for g, v in zip(groups, counts[k][0])] + [[name, from_int(counts[k][1])]])
                for k in order]
    return w.i, run


def v_count_similar(argv, i, o):
    w = FlagWalk("count-similar", argv, i)
    groups = []
    name = "count"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-g":
            groups = w.lst()
        elif opt == "-o":
            name = w.s()
        else:
            w.bad(opt)

    def run(recs):
        def key(rec):
            vals = selected(rec, groups)
            return None if vals is None else joined(vals)
        order, lists = group_lists(recs, key)
        out = []
        for k in order:
            for rec in lists[k]:
                rec.put(name, from_int(len(lists[k])))
                out.append(rec)
        return out
    return w.i, run


def record_string(rec):
    return "\x00".join(k + "\x01" + v.k + "\x01" + v.s for k, v in rec.f)


def uniq_like(verb, argv, i, o):
    w = FlagWalk(verb, argv, i)
    groups = None
    invert = False
    show_counts = show_n = all_fields = unlashed = False
    name = "count"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt in ("-g", "-f"):
            groups = w.lst()
        elif opt == "-x":
            groups = w.lst()
            invert = True
        elif opt == "-c":
            show_counts = True
        elif opt == "-n":
            show_n = True
        elif opt == "-o":
            name = w.s()
        elif opt == "-a":
            all_fields = True
        elif opt == "-u":
            unlashed = True
        else:
            w.bad(opt)
    if verb == "count-distinct":
        show_counts = not show_n

    def fields_for(rec):
        if invert:
            return [k for k in rec.keys() if k not in groups]
        return groups

    def run(recs):
        if all_fields:
            order = []
            counts = {}
            first = {}
            out = []
            for rec in recs:
                s = record_string(rec)
                if s not in counts:
                    counts[s] = 0
                    order.append(s)
                    first[s] = rec.copy()
                    if not show_counts and not show_n:
                        out.append(rec)
                counts[s] += 1
            if show_n:
                return [Rec([[name, from_int(len(order))]])]
            if show_counts:
                for s in order:
                    r = first[s]
                    r.prepend(name, from_int(counts[s]))
                    out.append(r)
            return out
        if unlashed:
            per = {}
            order = []
            for rec in recs:
                for f in fields_for(rec):
                    if f not in per:
                        per[f] = ([], {})
                        order.append(f)
                    v = rec.get(f)
                    if v is not None:
                        vorder, counts = per[f]
                        if v.s not in counts:
                            counts[v.s] = [v, 0]
                            vorder.append(v.s)
                        counts[v.s][1] += 1
            out = []
            for f in order:
                vorder, counts = per[f]
                for s in vorder:
                    out.append(Rec([["field", from_string(f)], ["value", counts[s][0]],
                                    ["count", from_int(counts[s][1])]]))
            return out
        order = []
        table = {}
        out = []
        for rec in recs:
            fs = fields_for(rec)
            vals = selected(rec, fs)
            if vals is None:
                continue
            key = joined(vals)
            if key not in table:
                table[key] = [fs, vals, 0]
                order.append(key)
                if not show_counts and not show_n:
                    out.append(Rec([[f, v] for f, v in zip(fs, vals)]))
            table[key][2] += 1
        if show_n:
            return [Rec([["count", from_int(len(order))]])]
        if show_counts:
            for key in order:
                fs, vals, c = table[key]
                out.append(Rec([[f, v] for f, v in zip(fs, vals)] + [[name, from_int(c)]]))
        return out
    return w.i, run


def v_uniq(argv, i, o):
    return uniq_like("uniq", argv, i, o)


def v_count_distinct(argv, i, o):
    return uniq_like("count-distinct", argv, i, o)


# ---------------------------------------------------------------- stats1, merge-fields


ACCUMULATORS = ["count", "null_count", "distinct_count", "mode", "antimode", "sum", "mean",
                "mad", "var", "stddev", "meaneb", "skewness", "kurtosis", "min", "max",
                "minlen", "maxlen"]


def percentile_of(name):
    if name == "median":
        return 50.0
    if name.startswith("p"):
        try:
            return float(name[1:])
        except ValueError:
            return None
    return None


def valid_acc(name):
    return name in ACCUMULATORS or percentile_of(name) is not None


class Acc:
    """One stats1 accumulator, as utils/stats1_accumulators.go keeps it."""

    def __init__(self, name, interp, keeper=None):
        self.name = name
        self.interp = interp
        self.keeper = keeper
        self.primary = False
        self.reset()

    def reset(self):
        self.count = 0
        self.sums = [from_int(0)] * 5
        self.vals = []
        self.counts = {}
        self.order = []
        self.m = ABSENT

    def ingest(self, v):
        n = self.name
        if n == "count":
            self.count += 1
        elif n == "null_count":
            if v.k == "void":
                self.count += 1
        elif n in ("distinct_count", "mode", "antimode"):
            if v.s not in self.counts:
                self.counts[v.s] = 0
                self.order.append(v.s)
            self.counts[v.s] += 1
        elif n in ("sum", "mean", "var", "stddev", "meaneb", "skewness", "kurtosis"):
            if is_num(v):
                self.count += 1
                p = v
                powers = [v]
                for _ in range(3):
                    p = times(v, p)
                    powers.append(p)
                self.sums[1] = plus(self.sums[1], v)
                for j in range(2, 5):
                    self.sums[j] = plus(self.sums[j], powers[j - 1])
        elif n == "mad":
            if is_num(v):
                self.vals.append(v)
        elif n == "min":
            self.m = bif_min(self.m, v)
        elif n == "max":
            self.m = bif_max(self.m, v)
        elif n == "minlen":
            self.m = bif_min(self.m, from_int(runes(v.s)))
        elif n == "maxlen":
            self.m = bif_max(self.m, from_int(runes(v.s)))
        elif self.primary:
            self.keeper.append(v)

    def emit(self):
        n = self.name
        if n in ("count", "null_count"):
            return from_int(self.count)
        if n == "distinct_count":
            return from_int(len(self.order))
        if n in ("mode", "antimode"):
            if not self.order:
                return VOID
            best = None
            bc = 0
            for s in self.order:
                c = self.counts[s]
                if best is None or (c > bc if n == "mode" else c < bc):
                    best, bc = s, c
            return from_string(best)
        if n == "sum":
            return self.sums[1]
        if n == "mean":
            return VOID if self.count == 0 else divide(self.sums[1], from_int(self.count))
        if n in ("var", "stddev", "meaneb"):
            var = finalize_var(self.count, self.sums[1], self.sums[2])
            if var.k == "void" or n == "var":
                return var
            if n == "stddev":
                return from_float(math.sqrt(var.n))
            return from_float(math.sqrt(fl(divide(var, from_int(self.count)))))
        if n == "kurtosis":
            if self.count < 2:
                return VOID
            fn = float(self.count)
            s1, s2, s3, s4 = (fl(x) for x in self.sums[1:5])
            mean = s1 / fn
            num = s4 - mean * (4.0 * s3 - mean * (6.0 * s2 - 3.0 * fn * mean * mean))
            num = num / fn
            den = (s2 - fn * mean * mean) / fn
            den = den * den
            return from_float(num / den - 3.0)
        if n == "mad":
            if not self.vals:
                return VOID
            mn = from_int(len(self.vals))
            mean = from_int(0)
            for v in self.vals:
                mean = plus(mean, v)
            mean = divide(mean, mn)
            dev = from_int(0)
            for v in self.vals:
                dev = plus(dev, bif_abs(minus(mean, v)))
            return divide(dev, mn)
        if n in ("min", "max", "minlen", "maxlen"):
            return VOID if self.m.k == "absent" else self.m
        return percentile(self.keeper, percentile_of(n), self.interp)


def finalize_var(count, msum, msum2):
    if count < 2:
        return VOID
    n = float(count)
    s, s2 = fl(msum), fl(msum2)
    mean = s / n
    num = s2 - mean * (2.0 * s - n * mean)
    if num < 0.0:
        num = 0.0
    return from_float(num / (n - 1.0))


def percentile(vals, p, interp):
    if not vals:
        return VOID
    arr = sorted(vals, key=cmp_to_key(cmp))
    n = len(arr)
    if not interp:
        idx = int(p * float(n) / 100.0)
        idx = min(max(idx, 0), n - 1)
        return arr[idx]
    findex = (p / 100.0) * (float(n) - 1)
    if findex < 0.0:
        findex = 0.0
    ii = int(math.floor(findex))
    if ii >= n - 1:
        return arr[ii]
    frac = from_float(findex - float(ii))
    return plus(arr[ii], times(frac, minus(arr[ii + 1], arr[ii])))


def make_accs(names, interp):
    """The percentile accumulators of one field share a keeper, and only the
    first of them (the primary) feeds it."""
    keeper = []
    out = []
    primary = True
    for a in names:
        acc = Acc(a, interp, keeper)
        if percentile_of(a) is not None:
            acc.primary = primary
            primary = False
        out.append((a, acc))
    return out


def v_stats1(argv, i, o):
    w = FlagWalk("stats1", argv, i)
    accs = None
    fields = None
    groups = []
    fregex = finvert = interp = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-a":
            accs = w.lst()
        elif opt == "-f":
            fields = w.lst()
        elif opt == "-g":
            groups = w.lst()
        elif opt == "--fr":
            fields = w.lst()
            fregex = True
        elif opt == "--fx":
            fields = w.lst()
            fregex = finvert = True
        elif opt == "-i":
            interp = True
        else:
            w.bad(opt)
    if accs is None:
        raise Fail("mlr stats1: -a option is required.\nPlease see mlr stats1 --help for more information.\n")
    if fields is None:
        raise Fail("mlr stats1: -f option is required.\nPlease see mlr stats1 --help for more information.\n")

    def build():
        for a in accs:
            if not valid_acc(a):
                raise Fail('mlr stats1: accumulator "%s" not found.\n' % a)
        rxs = [miller_regex(f) for f in fields] if fregex else None

        def run(recs):
            order = []
            table = {}
            for rec in recs:
                gv = selected(rec, groups)
                if gv is None:
                    continue
                key = joined(gv)
                if key not in table:
                    table[key] = (gv, [], {})
                    order.append(key)
                gv0, forder, level3 = table[key]
                if fregex:
                    names = [k for k in rec.keys()
                             if any(rx.search(k) for rx in rxs) != finvert]
                else:
                    names = fields
                for f in names:
                    v = rec.get(f)
                    if v is None:
                        continue
                    if f not in level3:
                        level3[f] = make_accs(accs, interp)
                        forder.append(f)
                    for a, acc in level3[f]:
                        if v.k == "void" and (fregex or a != "null_count"):
                            continue
                        acc.ingest(v)
            out = []
            for key in order:
                gv, forder, level3 = table[key]
                rec = Rec([[g, v] for g, v in zip(groups, gv)])
                for f in forder:
                    for a, acc in level3[f]:
                        rec.put(f + "_" + a, acc.emit())
                out.append(rec)
            return out
        return run
    return w.i, ("construct", build)


def v_merge_fields(argv, i, o):
    w = FlagWalk("merge-fields", argv, i)
    accs = None
    names = None
    mode = None
    out_name = None
    keep = interp = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-a":
            accs = w.lst()
        elif opt in ("-f", "-r", "-c"):
            names = w.lst()
            mode = opt
        elif opt == "-o":
            out_name = w.s()
        elif opt == "-k":
            keep = True
        elif opt == "-i":
            interp = True
        else:
            w.bad(opt)
    if accs is None:
        raise Fail("mlr merge-fields: -a option is required.\nPlease see mlr merge-fields --help for more information.\n")
    if names is None:
        raise Fail("mlr merge-fields: -f option is required.\nPlease see mlr merge-fields --help for more information.\n")

    def build():
        for a in accs:
            if not valid_acc(a):
                raise Fail('mlr merge-fields: accumulator "%s" not found.\n\n' % a)
        rxs = [miller_regex(n) for n in names] if mode != "-f" else None

        def run(recs):
            for rec in recs:
                if mode == "-c":
                    groups = []
                    table = {}
                    for p in list(rec.f):
                        k, v = p
                        short = None
                        for rx in rxs:
                            if rx.search(k):
                                short = rx.sub("", k, count=1)
                                break
                        if short is None:
                            continue
                        if short not in table:
                            table[short] = make_accs(accs, interp)
                            groups.append(short)
                        if v.k != "void":
                            for _, acc in table[short]:
                                acc.ingest(v)
                        if not keep:
                            rec.f.remove(p)
                    for short in groups:
                        for a, acc in table[short]:
                            rec.put(short + "_" + a, acc.emit())
                    continue
                named = make_accs(accs, interp)
                if mode == "-f":
                    targets = [n for n in names if rec.has(n)]
                else:
                    targets = [k for k in rec.keys() if any(rx.search(k) for rx in rxs)]
                for n in targets:
                    v = rec.get(n)
                    if v.k != "void":
                        for _, acc in named:
                            acc.ingest(v)
                    if not keep:
                        rec.remove(n)
                for a, acc in named:
                    rec.put(out_name + "_" + a, acc.emit())
            return recs
        return run
    return w.i, ("construct", build)


# ---------------------------------------------------------------- fraction


def v_fraction(argv, i, o):
    w = FlagWalk("fraction", argv, i)
    fields = []
    groups = []
    percent = cumu = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            fields = w.lst()
        elif opt == "-g":
            groups = w.lst()
        elif opt == "-p":
            percent = True
        elif opt == "-c":
            cumu = True
        else:
            w.bad(opt)
    mult = from_int(100 if percent else 1)
    suffix = ("_cumulative" if cumu else "") + ("_percent" if percent else "_fraction")
    zero = from_int(0)

    def run(recs):
        sums = {}
        cumus = {}
        for rec in recs:
            gv = selected(rec, groups)
            if gv is None:
                continue
            key = joined(gv)
            s = sums.setdefault(key, {})
            c = cumus.setdefault(key, {})
            for f in fields:
                v = rec.get(f)
                if v is None:
                    continue
                if f not in s:
                    s[f] = v
                    c[f] = zero
                else:
                    s[f] = plus(s[f], v)
        for rec in recs:
            gv = selected(rec, groups)
            if gv is None:
                continue
            key = joined(gv)
            for f in fields:
                v = rec.get(f)
                if v is None:
                    continue
                numer = plus(v, cumus[key][f]) if cumu else v
                den = sums[key][f]
                if cmp(numer, zero) == 0:
                    outv = zero
                else:
                    outv = times(divide(numer, den), mult)
                rec.put(f + suffix, outv)
                if cumu:
                    cumus[key][f] = plus(cumus[key][f], v)
        return recs
    return w.i, run


# ---------------------------------------------------------------- step


class Window:
    def __init__(self, back, fwd):
        self.back = [None] * back
        self.cur = None
        self.fwd = [None] * fwd

    def ingest(self, rec):
        if self.back:
            self.back = [self.cur] + self.back[:-1]
        if self.fwd:
            self.cur = self.fwd[0]
            self.fwd = self.fwd[1:] + [rec]
        else:
            self.cur = rec

    def get(self, i):
        if i == 0:
            return self.cur
        if i > 0:
            return self.fwd[i - 1]
        return self.back[-i - 1]


def stepper_shape(name):
    if name in ("delta", "shift", "shift_lag", "ratio"):
        return (1, 0)
    if name == "shift_lead":
        return (0, 1)
    if name in ("from-first", "rsum", "rprod", "counter", "ewma"):
        return (0, 0)
    m = re.match(r"^slwin_(\d+)_(\d+)\Z", name)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None


class Stepper:
    def __init__(self, name, field, alphas, suffixes):
        self.name = name
        self.field = field
        self.acc = from_int(1) if name == "rprod" else from_int(0)
        self.first = None
        self.alphas = [from_float(float(a)) for a in alphas]
        self.oneminus = [from_float(1.0 - float(a)) for a in alphas]
        sfx = suffixes if suffixes else alphas
        self.ewma_names = [field + "_ewma_" + s for s in sfx]
        self.prevs = None
        shape = stepper_shape(name)
        self.b, self.f = shape

    def process(self, win):
        cur = win.get(0)
        n = self.name
        f = self.field
        if n == "slwin_%d_%d" % (self.b, self.f) and n.startswith("slwin"):
            count = 0
            s = from_float(0.0)
            for j in range(-self.b, self.f + 1):
                r = win.get(j)
                if r is None:
                    continue
                v = r.get(f)
                if v.k == "void":
                    continue
                s = plus(s, v)
                count += 1
            if cur is None:
                return
            cur.put("%s_%d_%d" % (f, self.b, self.f), VOID if count == 0 else divide(s, from_int(count)))
            return
        if cur is None:
            return
        v = cur.get(f)
        if n == "delta":
            if v.k == "void":
                cur.put(f + "_delta", VOID)
                return
            d = from_int(0)
            prev = win.get(-1)
            if prev is not None and prev.get(f) is not None:
                d = minus(v, prev.get(f))
            cur.put(f + "_delta", d)
        elif n in ("shift", "shift_lag"):
            prev = win.get(-1)
            pv = None if prev is None else prev.get(f)
            cur.put(f + "_" + n, VOID if pv is None else pv)
        elif n == "shift_lead":
            nxt = win.get(1)
            if nxt is None:
                cur.put(f + "_shift_lead", VOID)
            elif nxt.get(f) is not None:
                cur.put(f + "_shift_lead", nxt.get(f))
        elif n == "from-first":
            out = from_int(0)
            if self.first is None:
                self.first = v
            else:
                out = minus(v, self.first)
            cur.put(f + "_from_first", out)
        elif n == "ratio":
            if v.k == "void":
                cur.put(f + "_ratio", VOID)
                return
            r = from_int(1)
            prev = win.get(-1)
            if prev is not None and prev.get(f) is not None:
                r = divide(v, prev.get(f))
            cur.put(f + "_ratio", r)
        elif n in ("rsum", "rprod", "counter"):
            if v.k == "void":
                cur.put(f + "_" + n, VOID)
                return
            if n == "rsum":
                self.acc = plus(v, self.acc)
            elif n == "rprod":
                self.acc = times(v, self.acc)
            else:
                self.acc = plus(self.acc, from_int(1))
            cur.put(f + "_" + n, self.acc)
        elif n == "ewma":
            if self.prevs is None:
                for name in self.ewma_names:
                    cur.put(name, v)
                self.prevs = [v for _ in self.alphas]
            else:
                for j, name in enumerate(self.ewma_names):
                    nxt = plus(times(v, self.alphas[j]), times(self.prevs[j], self.oneminus[j]))
                    cur.put(name, nxt)
                    self.prevs[j] = nxt


def v_step(argv, i, o):
    w = FlagWalk("step", argv, i)
    steppers = []
    fields = []
    groups = []
    alphas = []
    suffixes = []
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-a":
            for name in w.lst():
                if stepper_shape(name) is None:
                    raise Fail('mlr step: stepper "%s" not found.\n' % name)
                steppers.append(name)
        elif opt == "-f":
            fields += w.lst()
        elif opt == "-g":
            groups = w.lst()
        elif opt == "-d":
            alphas = w.lst()
        elif opt == "-o":
            suffixes = w.lst()
        else:
            w.bad(opt)

    def build():
        if not steppers or not fields:
            raise Fail("mlr step: -a and -f are both required arguments.\n")
        back = max(stepper_shape(s)[0] for s in steppers)
        fwd = max(stepper_shape(s)[1] for s in steppers)

        def run(recs):
            out = []
            windows = {}
            states = {}
            log = []
            for rec in recs:
                gv = selected(rec, groups)
                if gv is None:
                    out.append(rec)
                    continue
                key = joined(gv)
                if key not in windows:
                    windows[key] = Window(back, fwd)
                    states[key] = {}
                win = windows[key]
                win.ingest(rec)
                log.append((rec, key))
                for f in fields:
                    if rec.get(f) is None:
                        continue
                    st = states[key].setdefault(f, {})
                    for s in steppers:
                        if s not in st:
                            st[s] = Stepper(s, f, alphas, suffixes)
                        st[s].process(win)
                cur = win.get(0)
                if cur is not None:
                    out.append(cur)
                    log = [e for e in log if e[0] is not cur]
            for rec, key in log:
                win = windows[key]
                win.ingest(None)
                for f in fields:
                    if rec.get(f) is None:
                        continue
                    for s in steppers:
                        states[key][f][s].process(win)
                cur = win.get(0)
                if cur is not None:
                    out.append(cur)
            return out
        return run
    return w.i, ("construct", build)


# ---------------------------------------------------------------- nest


def v_nest(argv, i, o):
    w = FlagWalk("nest", argv, i)
    field = None
    action = what = across = None
    fs = ";"
    ps = ":"
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            field = w.s()
        elif opt in ("--explode", "-e"):
            action = "explode"
        elif opt in ("--implode", "-i"):
            action = "implode"
        elif opt in ("--values", "-v"):
            what = "values"
        elif opt in ("--pairs", "-p"):
            what = "pairs"
        elif opt in ("--across-records", "-R"):
            across = "records"
        elif opt in ("--across-fields", "-F"):
            across = "fields"
        elif opt in ("--nested-fs", "-S"):
            fs = sep(w.s())
        elif opt in ("--nested-ps", "-P"):
            ps = sep(w.s())
        elif opt == "--evar":
            fs = sep(w.s())
            action, what, across = "explode", "values", "records"
        elif opt == "--ivar":
            fs = sep(w.s())
            action, what, across = "implode", "values", "records"
        else:
            w.bad(opt)
    if field is None or action is None or what is None or across is None:
        raise Fail("mlr nest: missing required argument.\n")

    def explode_values_records(recs):
        out = []
        for rec in recs:
            v = rec.get(field)
            if v is None:
                out.append(rec)
                continue
            for piece in v.s.split(fs):
                r = rec.copy()
                r.put(field, from_string(piece))
                out.append(r)
        return out

    def explode_values_fields(recs):
        for rec in recs:
            at = rec.index(field)
            if at < 0:
                continue
            v = rec.f[at][1]
            pos = at
            for j, piece in enumerate(v.s.split(fs)):
                pos = rec.put_after(pos, "%s_%d" % (field, j + 1), from_string(piece))
            del rec.f[at]
        return recs

    def pieces_of(s):
        return [] if s == "" else s.split(fs)

    def explode_pairs_fields(recs):
        for rec in recs:
            at = rec.index(field)
            if at < 0:
                continue
            pos = at
            for piece in pieces_of(rec.f[at][1].s):
                pair = piece.split(ps, 1)
                if len(pair) == 2:
                    pos = rec.put_after(pos, pair[0], from_string(pair[1]))
                else:
                    pos = rec.put_after(pos, field, from_string(piece))
            del rec.f[at]
        return recs

    def explode_pairs_records(recs):
        out = []
        for rec in recs:
            v = rec.get(field)
            if v is None:
                out.append(rec)
                continue
            for piece in pieces_of(v.s):
                r = rec.copy()
                at = r.index(field)
                pair = piece.split(ps, 1)
                if len(pair) == 2:
                    r.put_after(at, pair[0], from_string(pair[1]))
                else:
                    r.put_after(at, field, from_string(piece))
                del r.f[at]
                out.append(r)
        return out

    def implode_fields(recs):
        rx = re.compile("^" + field + "_[0-9]+$")
        for rec in recs:
            parts = []
            first = None
            kept = []
            for j, p in enumerate(rec.f):
                if rx.search(p[0]):
                    if first is None:
                        first = len(kept)
                    parts.append(p[1].s)
                else:
                    kept.append(p)
            if parts:
                kept.insert(first, [field, from_string(fs.join(parts))])
            rec.f = kept
        return recs

    def implode_records(recs):
        out = []
        order = []
        buckets = {}
        for rec in recs:
            at = rec.index(field)
            if at < 0:
                out.append(rec)
                continue
            others = [p for j, p in enumerate(rec.f) if j != at]
            key = (",".join(k for k, _ in others), ",".join(v.s for _, v in others))
            if key not in buckets:
                buckets[key] = (rec, [])
                order.append(key)
            buckets[key][1].append(rec.f[at][1])
        okeys = []
        by_okey = {}
        for key in order:
            if key[0] not in by_okey:
                by_okey[key[0]] = []
                okeys.append(key[0])
            by_okey[key[0]].append(key)
        for ok in okeys:
            for key in by_okey[ok]:
                rep, vals = buckets[key]
                rep.put(field, from_string(fs.join(v.s for v in vals)))
                out.append(rep)
        return out

    table = {
        ("explode", "values", "records"): explode_values_records,
        ("explode", "values", "fields"): explode_values_fields,
        ("explode", "pairs", "records"): explode_pairs_records,
        ("explode", "pairs", "fields"): explode_pairs_fields,
        ("implode", "values", "fields"): implode_fields,
        ("implode", "values", "records"): implode_records,
    }
    return w.i, table[(action, what, across)]


# ---------------------------------------------------------------- reorder, rename, label


def v_reorder(argv, i, o):
    w = FlagWalk("reorder", argv, i)
    names = None
    regexes = False
    after = False
    center = ""
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            names = w.lst()
            regexes = False
        elif opt == "-r":
            names = w.lst()
            regexes = True
        elif opt == "-b":
            center = w.s()
            after = False
        elif opt == "-a":
            center = w.s()
            after = True
        elif opt == "-e":
            after = True
            center = ""
        else:
            w.bad(opt)
    rxs = [miller_regex(n) for n in names] if regexes else None

    def matches(k):
        return any(rx.search(k) for rx in rxs)

    def one(rec):
        if center == "":
            if regexes:
                hit = [p for p in rec.f if matches(p[0])]
                miss = [p for p in rec.f if not matches(p[0])]
                rec.f = (miss + hit) if after else (hit + miss)
                return rec
            if after:
                for n in names:
                    at = rec.index(n)
                    if at >= 0:
                        rec.f.append(rec.f.pop(at))
            else:
                for n in reversed(names):
                    at = rec.index(n)
                    if at >= 0:
                        rec.f.insert(0, rec.f.pop(at))
            return rec
        if not rec.has(center):
            return rec
        if regexes:
            hit = [p for p in rec.f if p[0] != center and matches(p[0])]
            hk = set(k for k, _ in hit)
            out = []
            for p in rec.f:
                if p[0] == center:
                    if after:
                        out.append(p)
                    out.extend(hit)
                    if not after:
                        out.append(p)
                elif p[0] not in hk:
                    out.append(p)
            rec.f = out
            return rec
        out = []
        ci = rec.index(center)
        for p in rec.f[:ci]:
            if p[0] not in names:
                out.append(p)
        listed = [[n, rec.get(n)] for n in names if rec.has(n)]
        if not after:
            out.extend(listed)
        out.append([center, rec.get(center)])
        if after:
            out.extend(listed)
        for p in rec.f[ci:]:
            if p[0] != center and p[0] not in names:
                out.append(p)
        rec.f = out
        return rec
    return w.i, lambda recs: [one(r) for r in recs]


def rename_in(rec, old, new):
    at = rec.index(old)
    if at < 0:
        return
    ex = rec.index(new)
    if ex < 0:
        rec.f[at][0] = new
    else:
        rec.f[ex][1] = rec.f[at][1]
        del rec.f[at]


def v_rename(argv, i, o):
    w = FlagWalk("rename", argv, i)
    regexes = gsub = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-r":
            regexes = True
        elif opt == "-g":
            regexes = gsub = True
        else:
            w.bad(opt)
    names = w.positional().split(",")
    if len(names) % 2 != 0:
        raise Fail("mlr rename: field-name list must have even length.\n")
    pairs = [(names[j], names[j + 1]) for j in range(0, len(names), 2)]

    def walk(rec, newname_of):
        """Visit each entry once, in order, as Miller's linked-list walk
        does: a rename onto an existing key unlinks the visited entry and
        the walk carries on from the entry after it."""
        j = 0
        while j < len(rec.f):
            p = rec.f[j]
            old = p[0]
            new = newname_of(old)
            if new is None or new == old:
                j += 1
                continue
            ex = rec.index(new)
            if ex < 0:
                p[0] = new
                j += 1
            else:
                rec.f[ex][1] = p[1]
                del rec.f[j]
                if ex < j:
                    pass

    def run(recs):
        for rec in recs:
            if not regexes:
                table = dict(pairs)
                walk(rec, lambda k: table.get(k))
            else:
                for rxs, repl in pairs:
                    rx = miller_regex(rxs)
                    walk(rec, lambda k: sub_captures(k, rx, repl, gsub))
        return recs
    return w.i, run


def v_label(argv, i, o):
    w = FlagWalk("label", argv, i)
    opt = w.next()
    if opt is not None:
        w.bad(opt)
    names = w.positional().split(",")

    def build():
        seen = set()
        for n in names:
            if n in seen:
                raise Fail('mlr label: labels must be unique; got duplicate "%s"\n' % n)
            seen.add(n)

        def run(recs):
            for rec in recs:
                head = rec.f[:len(names)]
                rest = rec.f[len(names):]
                out = [[names[j], p[1]] for j, p in enumerate(head)]
                have = set(names[:len(head)])
                for p in rest:
                    if p[0] in have:
                        continue
                    out.append(p)
                    have.add(p[0])
                rec.f = out
            return recs
        return run
    return w.i, ("construct", build)


# ---------------------------------------------------------------- join


def v_join(argv, i, o):
    w = FlagWalk("join", argv, i)
    left_file = None
    out_names = left_names = right_names = None
    left_keep = None
    lp = rp = ""
    pairs = True
    ul = ur = False
    while True:
        opt = w.next()
        if opt is None:
            break
        if opt == "-f":
            left_file = w.s()
        elif opt == "-j":
            out_names = w.lst()
        elif opt == "-l":
            left_names = w.lst()
        elif opt == "-r":
            right_names = w.lst()
        elif opt == "--lk":
            left_keep = w.lst()
        elif opt == "--lp":
            lp = w.s()
        elif opt == "--rp":
            rp = w.s()
        elif opt == "--np":
            pairs = False
        elif opt == "--ul":
            ul = True
        elif opt == "--ur":
            ur = True
        elif opt == "-u":
            pass
        else:
            w.bad(opt)
    if left_file is None:
        raise Fail("mlr join: need left file name\n")
    if not pairs and not ul and not ur:
        raise Fail("mlr join: all emit flags are unset; no output is possible.\n")
    if out_names is None:
        raise Fail("mlr join: need output field names\n")
    left_names = left_names or out_names
    right_names = right_names or out_names
    keep = None
    if left_keep is not None:
        keep = set(left_keep) | set(left_names)

    def run(recs):
        lefts, err = READERS[o.ifmt](left_file, read_text(left_file), o, 1)
        if err is not None:
            raise Fail("mlr :  " + err)
        border = []
        buckets = {}
        unpairable = []
        for lrec in lefts:
            if keep is not None:
                lrec.f = [p for p in lrec.f if p[0] in keep]
            vals = selected(lrec, left_names)
            if vals is None:
                unpairable.append(lrec)
                continue
            key = joined(vals)
            if key not in buckets:
                buckets[key] = [[], False]
                border.append(key)
            buckets[key][0].append(lrec)
        out = []
        for rrec in recs:
            vals = selected(rrec, right_names)
            if vals is None:
                if ur:
                    out.append(rrec)
                continue
            key = joined(vals)
            if key not in buckets:
                if ur:
                    out.append(rrec)
                continue
            buckets[key][1] = True
            if pairs:
                for lrec in buckets[key][0]:
                    rec = rrec.like([])
                    for ln, on in zip(left_names, out_names):
                        v = lrec.get(ln)
                        if v is not None:
                            rec.put(on, v)
                    for k, v in lrec.f:
                        if k not in left_names:
                            rec.put(lp + k, v)
                    for k, v in rrec.f:
                        if k not in right_names:
                            rec.put(rp + k, v)
                    out.append(rec)
        if ul:
            for key in border:
                if not buckets[key][1]:
                    out.extend(buckets[key][0])
            out.extend(unpairable)
        return out
    return w.i, run


VERBS = {
    "cat": v_cat, "head": v_head, "tail": v_tail, "tac": v_tac,
    "group-by": v_group_by, "group-like": v_group_like, "regularize": v_regularize,
    "sort-within-records": v_sort_within_records, "cut": v_cut,
    "having-fields": v_having_fields, "template": v_template, "unsparsify": v_unsparsify,
    "fill-down": v_fill_down, "fill-empty": v_fill_empty, "grep": v_grep,
    "decimate": v_decimate, "sec2gmt": v_sec2gmt, "seqgen": v_seqgen, "sort": v_sort,
    "top": v_top, "count": v_count, "count-similar": v_count_similar, "uniq": v_uniq,
    "count-distinct": v_count_distinct, "stats1": v_stats1, "merge-fields": v_merge_fields,
    "fraction": v_fraction, "step": v_step, "nest": v_nest, "reorder": v_reorder,
    "rename": v_rename, "label": v_label, "join": v_join,
}


# ================================================================ main


def parse(argv):
    """parseCommandLinePassOne, then the constructors of pass two."""
    argv = getoptify(argv)
    o = Opts()
    chain = []
    names = []
    i = 0
    first = True
    while i < len(argv):
        a = argv[i]
        if a.startswith("-"):
            if a in MAIN_FLAGS0:
                MAIN_FLAGS0[a](o)
                i += 1
            elif a in MAIN_FLAGS1 and i + 1 < len(argv):
                MAIN_FLAGS1[a](o, argv[i + 1])
                i += 2
            else:
                raise Fail('mlr: option "%s" not recognized.\nPlease run "mlr --help" for usage information.\n' % a)
        elif first or a == "then":
            if a == "then":
                i += 1
            if i >= len(argv):
                raise Fail("mlr: 'then' must have a verb after it.\n")
            verb = argv[i]
            if verb not in VERBS:
                raise Fail('mlr: verb "%s" not found. Please use "mlr --help" for a list.\n' % verb)
            first = False
            i, tr = VERBS[verb](argv, i, o)
            chain.append(tr)
            names.append(verb)
        else:
            break
    finalize(o)
    built = []
    for tr in chain:
        if isinstance(tr, tuple):
            tr = tr[1]()
        built.append(tr)
    files = o.files + argv[i:]
    if names[0] == "seqgen" or o.no_input:
        files = []
    return o, built, names, files


def run_job(argv):
    """Returns (stdout, stderr or None)."""
    try:
        o, chain, names, files = parse(argv)
    except Fail as e:
        return "", str(e)
    recs, ierr = read_inputs(files, o)
    try:
        for tr in chain:
            recs = tr(recs)
    except Fail as e:
        return "", str(e)
    if o.ofmt == "json" and o.ifmt != "json" and o.auto_unflatten and names[-1] != "flatten":
        recs = [unflatten(r) for r in recs]
    text, werr = WRITERS[o.ofmt](recs, o)
    if werr is not None:
        return text, werr + "mlr: exiting due to data error.\n"
    if ierr is not None:
        return text, "mlr: %s.\n" % ierr
    return text, None


def shown(a):
    if a != "" and all(c.isascii() and (c.isalnum() or c in "@%+=:,./-_") for c in a):
        return a
    return "'" + a.replace("'", "'\"'\"'") + "'"


def main():
    with open(os.path.join(HERE, "data", "jobs.txt"), encoding="utf-8") as f:
        jobs = [l for l in f.read().split("\n") if l]
    for line in jobs:
        argv = line.split("\t")
        emit("$ mlr " + " ".join(shown(a) for a in argv) + "\n")
        out, err = run_job(argv)
        # A carriage return is shown as ^M, as `cat -v` shows it.
        out = out.replace("\r", "^M")
        emit(out)
        if out and not out.endswith("\n"):
            emit("\n\\ no newline at end of output\n")
        if err is not None:
            if err.endswith("\n"):
                err = err[:-1]
            for l in err.split("\n"):
                emit(("! " + l if l else "!") + "\n")
            emit("[exit 1]\n")
    sys.stdout.write("".join(OUT))


main()
