# An independent Python port of semver 7.7.2 (the npm package), its
# `semver` command-line tool, and the `lib` and `outdated` jobs that
# real.js runs. It reads data/jobs.txt and writes what real.js writes.
# Run from the app's directory: python3 oracle.py [data-dir]
import functools, json, os, re, sys

DATA = sys.argv[1] if len(sys.argv) > 1 else "data"
MAX_LENGTH = 256
MAX_SAFE_INTEGER = 9007199254740991
MAX_SAFE_COMPONENT_LENGTH = 16
MAX_SAFE_BUILD_LENGTH = MAX_LENGTH - 6

# --- the regular expressions, built from the same sources as re.js

LDN = "[a-zA-Z0-9-]"
SAFE = [("\\s", 1), ("\\d", MAX_LENGTH), (LDN, MAX_SAFE_BUILD_LENGTH)]


def make_safe(v):
    for tok, mx in SAFE:
        v = v.replace(tok + "*", tok + "{0,%d}" % mx).replace(tok + "+", tok + "{1,%d}" % mx)
    return v


src = {}
rx = {}


def tok(name, value):
    src[name] = value
    rx[name] = re.compile(make_safe(value), re.ASCII)


tok("NUMERICIDENTIFIER", "0|[1-9]\\d*")
tok("NUMERICIDENTIFIERLOOSE", "\\d+")
tok("NONNUMERICIDENTIFIER", "\\d*[a-zA-Z-]" + LDN + "*")
tok("MAINVERSION", "(%s)\\.(%s)\\.(%s)" % ((src["NUMERICIDENTIFIER"],) * 3))
tok("MAINVERSIONLOOSE", "(%s)\\.(%s)\\.(%s)" % ((src["NUMERICIDENTIFIERLOOSE"],) * 3))
tok("PRERELEASEIDENTIFIER", "(?:%s|%s)" % (src["NONNUMERICIDENTIFIER"], src["NUMERICIDENTIFIER"]))
tok("PRERELEASEIDENTIFIERLOOSE", "(?:%s|%s)" % (src["NONNUMERICIDENTIFIER"], src["NUMERICIDENTIFIERLOOSE"]))
tok("PRERELEASE", "(?:-(%s(?:\\.%s)*))" % (src["PRERELEASEIDENTIFIER"], src["PRERELEASEIDENTIFIER"]))
tok("PRERELEASELOOSE", "(?:-?(%s(?:\\.%s)*))" % (src["PRERELEASEIDENTIFIERLOOSE"], src["PRERELEASEIDENTIFIERLOOSE"]))
tok("BUILDIDENTIFIER", LDN + "+")
tok("BUILD", "(?:\\+(%s(?:\\.%s)*))" % (src["BUILDIDENTIFIER"], src["BUILDIDENTIFIER"]))
tok("FULLPLAIN", "v?%s%s?%s?" % (src["MAINVERSION"], src["PRERELEASE"], src["BUILD"]))
tok("FULL", "^%s$" % src["FULLPLAIN"])
tok("LOOSEPLAIN", "[v=\\s]*%s%s?%s?" % (src["MAINVERSIONLOOSE"], src["PRERELEASELOOSE"], src["BUILD"]))
tok("LOOSE", "^%s$" % src["LOOSEPLAIN"])
tok("GTLT", "((?:<|>)?=?)")
tok("XRANGEIDENTIFIERLOOSE", src["NUMERICIDENTIFIERLOOSE"] + "|x|X|\\*")
tok("XRANGEIDENTIFIER", src["NUMERICIDENTIFIER"] + "|x|X|\\*")
for suf, pre in (("", "PRERELEASE"), ("LOOSE", "PRERELEASELOOSE")):
    xi = src["XRANGEIDENTIFIER" + suf]
    tok("XRANGEPLAIN" + suf, "[v=\\s]*(%s)(?:\\.(%s)(?:\\.(%s)(?:%s)?%s?)?)?" % (xi, xi, xi, src[pre], src["BUILD"]))
tok("XRANGE", "^%s\\s*%s$" % (src["GTLT"], src["XRANGEPLAIN"]))
tok("XRANGELOOSE", "^%s\\s*%s$" % (src["GTLT"], src["XRANGEPLAINLOOSE"]))
D16 = "\\d{1,%d}" % MAX_SAFE_COMPONENT_LENGTH
tok("COERCEPLAIN", "(^|[^\\d])(%s)(?:\\.(%s))?(?:\\.(%s))?" % (D16, D16, D16))
tok("COERCE", src["COERCEPLAIN"] + "(?:$|[^\\d])")
tok("COERCEFULL", src["COERCEPLAIN"] + "(?:%s)?(?:%s)?(?:$|[^\\d])" % (src["PRERELEASE"], src["BUILD"]))
tok("LONETILDE", "(?:~>?)")
tok("TILDETRIM", "(\\s*)%s\\s+" % src["LONETILDE"])
tok("TILDE", "^%s%s$" % (src["LONETILDE"], src["XRANGEPLAIN"]))
tok("TILDELOOSE", "^%s%s$" % (src["LONETILDE"], src["XRANGEPLAINLOOSE"]))
tok("LONECARET", "(?:\\^)")
tok("CARETTRIM", "(\\s*)%s\\s+" % src["LONECARET"])
tok("CARET", "^%s%s$" % (src["LONECARET"], src["XRANGEPLAIN"]))
tok("CARETLOOSE", "^%s%s$" % (src["LONECARET"], src["XRANGEPLAINLOOSE"]))
tok("COMPARATORLOOSE", "^%s\\s*(%s)$|^$" % (src["GTLT"], src["LOOSEPLAIN"]))
tok("COMPARATOR", "^%s\\s*(%s)$|^$" % (src["GTLT"], src["FULLPLAIN"]))
tok("COMPARATORTRIM", "(\\s*)%s\\s*(%s|%s)" % (src["GTLT"], src["LOOSEPLAIN"], src["XRANGEPLAIN"]))
tok("HYPHENRANGE", "^\\s*(%s)\\s+-\\s+(%s)\\s*$" % (src["XRANGEPLAIN"], src["XRANGEPLAIN"]))
tok("HYPHENRANGELOOSE", "^\\s*(%s)\\s+-\\s+(%s)\\s*$" % (src["XRANGEPLAINLOOSE"], src["XRANGEPLAINLOOSE"]))
tok("STAR", "(<|>)?=?\\s*\\*")
tok("GTE0", "^\\s*>=\\s*0\\.0\\.0\\s*$")
tok("GTE0PRE", "^\\s*>=\\s*0\\.0\\.0-0\\s*$")

WS = re.compile(r"\s+", re.ASCII)
NUMERIC = re.compile(r"^[0-9]+$")


def js_trim(s):
    return s.strip(" \t\n\r\f\v")


def g(m, i):
    # A capture group as JS sees it: None when it did not take part.
    return m.group(i)


def sub_first(name, s, fn):
    m = rx[name].search(s)
    if not m:
        return s
    return s[:m.start()] + fn(m) + s[m.end():]


def sub_all(name, s, fn):
    return rx[name].sub(fn, s)


def num_str(n):
    return str(n)


def js_num(s):
    # Number(s) for the strings a version can hold: (is_nan, value).
    if s is None:
        return (True, 0)
    if s is False:
        return (False, 0)
    t = js_trim(s)
    if t == "":
        return (False, 0)
    if t in ("Infinity", "-Infinity", "+Infinity"):
        return (False, 1)
    for p, base in (("0x", 16), ("0o", 8), ("0b", 2)):
        if t[:2].lower() == p and len(t) > 2:
            try:
                return (False, int(t[2:], base))
            except ValueError:
                return (True, 0)
    if re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", t):
        return (False, float(t))
    return (True, 0)


# --- identifiers: a prerelease id is an int (numeric) or a str

def is_numeric(a):
    return isinstance(a, int) or bool(NUMERIC.match(a))


def compare_ids(a, b):
    anum = is_numeric(a)
    bnum = is_numeric(b)
    if anum and bnum:
        a = int(a)
        b = int(b)
    if a == b and type(a) == type(b):
        return 0
    if anum and not bnum:
        return -1
    if bnum and not anum:
        return 1
    if anum and bnum:
        return -1 if a < b else 1
    return -1 if str(a) < str(b) else 1


class VersionError(Exception):
    pass


class SemVer:
    def __init__(self, version, loose=False, incpre=False):
        if isinstance(version, SemVer):
            version = version.version
        if version is None:
            raise VersionError('Invalid version. Must be a string. Got type "undefined".')
        if len(version) > MAX_LENGTH:
            raise VersionError("version is longer than %d characters" % MAX_LENGTH)
        self.loose = loose
        self.incpre = incpre
        m = rx["LOOSE" if loose else "FULL"].search(js_trim(version))
        if not m:
            raise VersionError("Invalid Version: " + version)
        self.raw = version
        self.major = int(m.group(1))
        self.minor = int(m.group(2))
        self.patch = int(m.group(3))
        for n, what in ((self.major, "major"), (self.minor, "minor"), (self.patch, "patch")):
            if n > MAX_SAFE_INTEGER:
                raise VersionError("Invalid %s version" % what)
        self.prerelease = []
        if m.group(4):
            for id in m.group(4).split("."):
                if NUMERIC.match(id) and int(id) < MAX_SAFE_INTEGER:
                    self.prerelease.append(int(id))
                else:
                    self.prerelease.append(id)
        self.build = m.group(5).split(".") if m.group(5) else []
        self.format()

    def format(self):
        self.version = "%d.%d.%d" % (self.major, self.minor, self.patch)
        if self.prerelease:
            self.version += "-" + ".".join(str(x) for x in self.prerelease)
        return self.version

    def compare(self, other):
        if not isinstance(other, SemVer):
            if other == self.version:
                return 0
            other = SemVer(other, self.loose, self.incpre)
        if other.version == self.version:
            return 0
        return self.compare_main(other) or self.compare_pre(other)

    def compare_main(self, o):
        return compare_ids(self.major, o.major) or compare_ids(self.minor, o.minor) or compare_ids(self.patch, o.patch)

    def compare_pre(self, o):
        if self.prerelease and not o.prerelease:
            return -1
        if not self.prerelease and o.prerelease:
            return 1
        if not self.prerelease and not o.prerelease:
            return 0
        return compare_lists(self.prerelease, o.prerelease)

    def compare_build(self, o):
        return compare_lists(self.build, o.build)

    def inc(self, release, ident, base):
        if release.startswith("pre"):
            if not ident and base is False:
                raise VersionError("invalid increment argument: identifier is empty")
            if ident:
                m = rx["PRERELEASELOOSE" if self.loose else "PRERELEASE"].search("-" + ident)
                if not m or m.group(1) != ident:
                    raise VersionError("invalid identifier: " + ident)
        if release == "premajor":
            self.prerelease = []
            self.patch = 0
            self.minor = 0
            self.major += 1
            self.inc("pre", ident, base)
        elif release == "preminor":
            self.prerelease = []
            self.patch = 0
            self.minor += 1
            self.inc("pre", ident, base)
        elif release == "prepatch":
            self.prerelease = []
            self.inc("patch", ident, base)
            self.inc("pre", ident, base)
        elif release == "prerelease":
            if not self.prerelease:
                self.inc("patch", ident, base)
            self.inc("pre", ident, base)
        elif release == "release":
            if not self.prerelease:
                raise VersionError("version %s is not a prerelease" % self.raw)
            self.prerelease = []
        elif release == "major":
            if self.minor != 0 or self.patch != 0 or not self.prerelease:
                self.major += 1
            self.minor = 0
            self.patch = 0
            self.prerelease = []
        elif release == "minor":
            if self.patch != 0 or not self.prerelease:
                self.minor += 1
            self.patch = 0
            self.prerelease = []
        elif release == "patch":
            if not self.prerelease:
                self.patch += 1
            self.prerelease = []
        elif release == "pre":
            nan, val = js_num(base)
            b = 1 if (not nan and val != 0) else 0
            if not self.prerelease:
                self.prerelease = [b]
            else:
                i = len(self.prerelease) - 1
                done = False
                while i >= 0:
                    if isinstance(self.prerelease[i], int):
                        self.prerelease[i] += 1
                        done = True
                        break
                    i -= 1
                if not done:
                    if ident == ".".join(str(x) for x in self.prerelease) and base is False:
                        raise VersionError("invalid increment argument: identifier already exists")
                    self.prerelease.append(b)
            if ident:
                pre = [ident, b]
                if base is False:
                    pre = [ident]
                if compare_ids(self.prerelease[0], ident) == 0:
                    second = self.prerelease[1] if len(self.prerelease) > 1 else None
                    if second is None or (isinstance(second, str) and js_num(second)[0]):
                        self.prerelease = pre
                else:
                    self.prerelease = pre
        else:
            raise VersionError("invalid increment argument: " + release)
        self.raw = self.format()
        if self.build:
            self.raw += "+" + ".".join(self.build)
        return self


def compare_lists(a, b):
    i = 0
    while True:
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x is None and y is None:
            return 0
        if y is None:
            return 1
        if x is None:
            return -1
        if not (x == y and type(x) == type(y)):
            return compare_ids(x, y)
        i += 1


def parse(v, loose=False, incpre=False):
    try:
        return SemVer(v, loose, incpre)
    except VersionError:
        return None


def valid(v, loose=False, incpre=False):
    p = parse(v, loose, incpre)
    return p.version if p else None


def compare(a, b, loose=False, incpre=False):
    return SemVer(a, loose, incpre).compare(SemVer(b, loose, incpre))


def cmp(a, op, b):
    c = a.compare(b)
    if op == "":
        return c == 0
    if op == ">":
        return c > 0
    if op == ">=":
        return c >= 0
    if op == "<":
        return c < 0
    if op == "<=":
        return c <= 0
    raise VersionError("Invalid operator: " + op)


# --- comparators and ranges

ANY = None


class Comparator:
    def __init__(self, comp, loose=False):
        comp = " ".join(WS.split(js_trim(comp)))
        self.loose = loose
        m = rx["COMPARATORLOOSE" if loose else "COMPARATOR"].search(comp)
        if not m:
            raise VersionError("Invalid comparator: " + comp)
        self.operator = m.group(1) if m.group(1) is not None else ""
        if self.operator == "=":
            self.operator = ""
        if not m.group(2):
            self.semver = ANY
            self.value = ""
        else:
            self.semver = SemVer(m.group(2), loose)
            self.value = self.operator + self.semver.version

    def test(self, version):
        if self.semver is ANY:
            return True
        return cmp(version, self.operator, self.semver)

    def intersects(self, comp, loose, incpre):
        if self.operator == "":
            if self.value == "":
                return True
            return Range(comp.value, loose, incpre).test(self.value)
        elif comp.operator == "":
            if comp.value == "":
                return True
            return Range(self.value, loose, incpre).test(comp.semver)
        if incpre and (self.value == "<0.0.0-0" or comp.value == "<0.0.0-0"):
            return False
        if not incpre and (self.value.startswith("<0.0.0") or comp.value.startswith("<0.0.0")):
            return False
        if self.operator.startswith(">") and comp.operator.startswith(">"):
            return True
        if self.operator.startswith("<") and comp.operator.startswith("<"):
            return True
        if self.semver.version == comp.semver.version and "=" in self.operator and "=" in comp.operator:
            return True
        if cmp(self.semver, "<", comp.semver) and self.operator.startswith(">") and comp.operator.startswith("<"):
            return True
        if cmp(self.semver, ">", comp.semver) and self.operator.startswith("<") and comp.operator.startswith(">"):
            return True
        return False


def is_x(id):
    return not id or id.lower() == "x" or id == "*"


def js_plus1(s):
    return str(int(s) + 1)


def replace_caret(comp, loose, incpre):
    z = "-0" if incpre else ""

    def fn(mt):
        M, m, p, pr = g(mt, 1), g(mt, 2), g(mt, 3), g(mt, 4)
        if is_x(M):
            return ""
        if is_x(m):
            return ">=%s.0.0%s <%s.0.0-0" % (M, z, js_plus1(M))
        if is_x(p):
            if M == "0":
                return ">=%s.%s.0%s <%s.%s.0-0" % (M, m, z, M, js_plus1(m))
            return ">=%s.%s.0%s <%s.0.0-0" % (M, m, z, js_plus1(M))
        if pr:
            if M == "0":
                if m == "0":
                    return ">=%s.%s.%s-%s <%s.%s.%s-0" % (M, m, p, pr, M, m, js_plus1(p))
                return ">=%s.%s.%s-%s <%s.%s.0-0" % (M, m, p, pr, M, js_plus1(m))
            return ">=%s.%s.%s-%s <%s.0.0-0" % (M, m, p, pr, js_plus1(M))
        if M == "0":
            if m == "0":
                return ">=%s.%s.%s%s <%s.%s.%s-0" % (M, m, p, z, M, m, js_plus1(p))
            return ">=%s.%s.%s%s <%s.%s.0-0" % (M, m, p, z, M, js_plus1(m))
        return ">=%s.%s.%s <%s.0.0-0" % (M, m, p, js_plus1(M))

    return sub_first("CARETLOOSE" if loose else "CARET", comp, fn)


def replace_tilde(comp, loose):
    def fn(mt):
        M, m, p, pr = g(mt, 1), g(mt, 2), g(mt, 3), g(mt, 4)
        if is_x(M):
            return ""
        if is_x(m):
            return ">=%s.0.0 <%s.0.0-0" % (M, js_plus1(M))
        if is_x(p):
            return ">=%s.%s.0 <%s.%s.0-0" % (M, m, M, js_plus1(m))
        if pr:
            return ">=%s.%s.%s-%s <%s.%s.0-0" % (M, m, p, pr, M, js_plus1(m))
        return ">=%s.%s.%s <%s.%s.0-0" % (M, m, p, M, js_plus1(m))

    return sub_first("TILDELOOSE" if loose else "TILDE", comp, fn)


def replace_xrange(comp, loose, incpre):
    comp = js_trim(comp)

    def fn(mt):
        ret = mt.group(0)
        gtlt, M, m, p = g(mt, 1), g(mt, 2), g(mt, 3), g(mt, 4)
        xM = is_x(M)
        xm = xM or is_x(m)
        xp = xm or is_x(p)
        anyX = xp
        if gtlt == "=" and anyX:
            gtlt = ""
        pr = "-0" if incpre else ""
        if xM:
            if gtlt == ">" or gtlt == "<":
                ret = "<0.0.0-0"
            else:
                ret = "*"
        elif gtlt and anyX:
            if xm:
                m = "0"
            p = "0"
            if gtlt == ">":
                gtlt = ">="
                if xm:
                    M = js_plus1(M)
                    m = "0"
                    p = "0"
                else:
                    m = js_plus1(m)
                    p = "0"
            elif gtlt == "<=":
                gtlt = "<"
                if xm:
                    M = js_plus1(M)
                else:
                    m = js_plus1(m)
            if gtlt == "<":
                pr = "-0"
            ret = "%s%s.%s.%s%s" % (gtlt, M, m, p, pr)
        elif xm:
            ret = ">=%s.0.0%s <%s.0.0-0" % (M, pr, js_plus1(M))
        elif xp:
            ret = ">=%s.%s.0%s <%s.%s.0-0" % (M, m, pr, M, js_plus1(m))
        return ret

    return sub_first("XRANGELOOSE" if loose else "XRANGE", comp, fn)


def parse_comparator(comp, loose, incpre):
    comp = " ".join(replace_caret(c, loose, incpre) for c in WS.split(js_trim(comp)))
    comp = " ".join(replace_tilde(c, loose) for c in WS.split(js_trim(comp)))
    comp = " ".join(replace_xrange(c, loose, incpre) for c in WS.split(comp))
    comp = sub_first("STAR", js_trim(comp), lambda m: "")
    return comp


def hyphen_replace(incpre):
    def fn(mt):
        frm, fM, fm, fp, fpr = g(mt, 1), g(mt, 2), g(mt, 3), g(mt, 4), g(mt, 5)
        to, tM, tm, tp, tpr = g(mt, 7), g(mt, 8), g(mt, 9), g(mt, 10), g(mt, 11)
        z = "-0" if incpre else ""
        if is_x(fM):
            frm = ""
        elif is_x(fm):
            frm = ">=%s.0.0%s" % (fM, z)
        elif is_x(fp):
            frm = ">=%s.%s.0%s" % (fM, fm, z)
        elif fpr:
            frm = ">=" + frm
        else:
            frm = ">=%s%s" % (frm, z)
        if is_x(tM):
            to = ""
        elif is_x(tm):
            to = "<%s.0.0-0" % js_plus1(tM)
        elif is_x(tp):
            to = "<%s.%s.0-0" % (tM, js_plus1(tm))
        elif tpr:
            to = "<=%s.%s.%s-%s" % (tM, tm, tp, tpr)
        elif incpre:
            to = "<%s.%s.%s-0" % (tM, tm, js_plus1(tp))
        else:
            to = "<=" + to
        return js_trim(frm + " " + to)

    return fn


def trim_repl(m):
    return "".join(m.group(i) or "" for i in (1, 2, 3))


class Range:
    def __init__(self, rng, loose=False, incpre=False):
        self.loose = loose
        self.incpre = incpre
        self.raw = WS.sub(" ", js_trim(rng))
        sets = [self.parse_range(js_trim(r)) for r in self.raw.split("||")]
        sets = [c for c in sets if c]
        if not sets:
            raise VersionError("Invalid SemVer Range: " + self.raw)
        if len(sets) > 1:
            first = sets[0]
            sets = [c for c in sets if c[0].value != "<0.0.0-0"]
            if not sets:
                sets = [first]
            elif len(sets) > 1:
                for c in sets:
                    if len(c) == 1 and c[0].value == "":
                        sets = [c]
                        break
        self.set = sets

    def range(self):
        return "||".join(" ".join(js_trim(c.value) for c in comps) for comps in self.set)

    def parse_range(self, r):
        loose, incpre = self.loose, self.incpre
        r = sub_first("HYPHENRANGELOOSE" if loose else "HYPHENRANGE", r, hyphen_replace(incpre))
        r = sub_all("COMPARATORTRIM", r, trim_repl)
        r = sub_all("TILDETRIM", r, lambda m: (m.group(1) or "") + "~")
        r = sub_all("CARETTRIM", r, lambda m: (m.group(1) or "") + "^")
        lst = " ".join(parse_comparator(c, loose, incpre) for c in r.split(" "))
        lst = [sub_first("GTE0PRE" if incpre else "GTE0", js_trim(c), lambda m: "") for c in WS.split(lst)]
        if loose:
            lst = [c for c in lst if rx["COMPARATORLOOSE"].search(c)]
        comps = {}
        for c in lst:
            comp = Comparator(c, loose)
            if comp.value == "<0.0.0-0":
                return [comp]
            comps[comp.value] = comp
        if len(comps) > 1 and "" in comps:
            del comps[""]
        return list(comps.values())

    def test(self, version):
        if not version:
            return False
        if not isinstance(version, SemVer):
            try:
                version = SemVer(version, self.loose, self.incpre)
            except VersionError:
                return False
        return any(test_set(s, version, self.incpre) for s in self.set)

    def intersects(self, other, loose, incpre):
        for a in self.set:
            if not satisfiable(a, loose, incpre):
                continue
            for b in other.set:
                if satisfiable(b, loose, incpre) and all(x.intersects(y, loose, incpre) for x in a for y in b):
                    return True
        return False


def satisfiable(comps, loose, incpre):
    result = True
    rest = comps[:]
    t = rest.pop()
    while result and rest:
        result = all(t.intersects(o, loose, incpre) for o in rest)
        t = rest.pop()
    return result


def test_set(s, version, incpre):
    for c in s:
        if not c.test(version):
            return False
    if version.prerelease and not incpre:
        for c in s:
            if c.semver is ANY:
                continue
            if c.semver.prerelease:
                a = c.semver
                if a.major == version.major and a.minor == version.minor and a.patch == version.patch:
                    return True
        return False
    return True


def satisfies(v, rng, loose=False, incpre=False):
    try:
        r = Range(rng, loose, incpre)
    except VersionError:
        return False
    return r.test(v)


def valid_range(rng, loose=False, incpre=False):
    try:
        return Range(rng, loose, incpre).range() or "*"
    except VersionError:
        return None


def max_satisfying(versions, rng, loose, incpre, want):
    try:
        r = Range(rng, loose, incpre)
    except VersionError:
        return None
    best = None
    best_sv = None
    for v in versions:
        if r.test(v):
            if best is None or best_sv.compare(v) == want:
                best = v
                best_sv = SemVer(v, loose, incpre)
    return best


def min_version(rng, loose, incpre):
    r = Range(rng, loose, incpre)
    for start in ("0.0.0", "0.0.0-0"):
        mv = SemVer(start)
        if r.test(mv):
            return mv
    mv = None
    for comps in r.set:
        set_min = None
        for c in comps:
            cv = SemVer(c.semver.version if c.semver is not ANY else None)
            op = c.operator
            if op == ">":
                if not cv.prerelease:
                    cv.patch += 1
                else:
                    cv.prerelease.append(0)
                cv.raw = cv.format()
            if op in (">", "", ">="):
                if set_min is None or cv.compare(set_min) > 0:
                    set_min = cv
        if set_min is not None and (mv is None or mv.compare(set_min) > 0):
            mv = set_min
    if mv is not None and r.test(mv):
        return mv
    return None


def intersects(r1, r2, loose, incpre):
    a = Range(r1, loose, incpre)
    b = Range(r2, loose, incpre)
    return a.intersects(b, loose, incpre)


def diff(a, b):
    v1 = SemVer(a)
    v2 = SemVer(b)
    c = v1.compare(v2)
    if c == 0:
        return None
    high, low = (v1, v2) if c > 0 else (v2, v1)
    hp = bool(high.prerelease)
    lp = bool(low.prerelease)
    if lp and not hp:
        if not low.patch and not low.minor:
            return "major"
        if low.compare_main(high) == 0:
            if low.minor and not low.patch:
                return "minor"
            return "patch"
    prefix = "pre" if hp else ""
    if v1.major != v2.major:
        return prefix + "major"
    if v1.minor != v2.minor:
        return prefix + "minor"
    if v1.patch != v2.patch:
        return prefix + "patch"
    return "prerelease"


def sort_stable(xs, key_cmp):
    return sorted(xs, key=functools.cmp_to_key(key_cmp))


def simplify(versions, rng, loose, incpre):
    v = sort_stable(versions, lambda a, b: compare(a, b, loose, incpre))
    sets = []
    first = None
    prev = None
    for ver in v:
        if satisfies(ver, rng, loose, incpre):
            prev = ver
            if first is None:
                first = ver
        else:
            if prev is not None:
                sets.append((first, prev))
            prev = None
            first = None
    if first is not None:
        sets.append((first, None))
    out = []
    for lo, hi in sets:
        if lo == hi:
            out.append(lo)
        elif hi is None and lo == v[0]:
            out.append("*")
        elif hi is None:
            out.append(">=" + lo)
        elif lo == v[0]:
            out.append("<=" + hi)
        else:
            out.append("%s - %s" % (lo, hi))
    s = " || ".join(out)
    return s if len(s) < len(rng) else rng


def coerce(version, loose, incpre, rtl):
    match = None
    if not rtl:
        match = rx["COERCEFULL" if incpre else "COERCE"].search(version)
    else:
        r = rx["COERCEFULL" if incpre else "COERCE"]
        pos = 0
        while True:
            nxt = r.search(version, pos)
            if not nxt:
                break
            if match and match.end() == len(version):
                break
            if not match or nxt.end() != match.end():
                match = nxt
            pos = nxt.start() + len(nxt.group(1)) + len(nxt.group(2))
    if match is None:
        return None
    major = match.group(2)
    minor = match.group(3) or "0"
    patch = match.group(4) or "0"
    pre = "-" + match.group(5) if incpre and match.group(5) else ""
    bld = "+" + match.group(6) if incpre and match.group(6) else ""
    return parse("%s.%s.%s%s%s" % (major, minor, patch, pre, bld), loose, incpre)


def inc(v, release, loose, incpre, ident, base):
    try:
        return SemVer(v, loose, incpre).inc(release, ident, base).version
    except VersionError:
        return None


# --- the command-line tool

HELP = """SemVer 7.7.2

A JavaScript implementation of the https://semver.org/ specification
Copyright Isaac Z. Schlueter

Usage: semver [options] <version> [<version> [...]]
Prints valid versions sorted by SemVer precedence

Options:
-r --range <range>
        Print versions that match the specified range.

-i --increment [<level>]
        Increment a version by the specified level.  Level can
        be one of: major, minor, patch, premajor, preminor,
        prepatch, prerelease, or release.  Default level is 'patch'.
        Only one version may be specified.

--preid <identifier>
        Identifier to be used to prefix premajor, preminor,
        prepatch or prerelease version increments.

-l --loose
        Interpret versions and ranges loosely

-p --include-prerelease
        Always include prerelease versions in range matching

-c --coerce
        Coerce a string into SemVer if possible
        (does not imply --loose)

--rtl
        Coerce version strings right to left

--ltr
        Coerce version strings left to right (default)

-n <base>
        Base number to be used for the prerelease identifier.
        Can be either 0 or 1, or false to omit the number altogether.
        Defaults to 0.

Program exits successfully if any valid version satisfies
all supplied ranges, and prints all satisfying versions.

If no satisfying versions are found, then exits failure.

Versions are printed in ascending order, so supplying
multiple versions to the utility will just sort them.
"""

LEVELS = ("major", "minor", "patch", "prerelease", "premajor", "preminor", "prepatch", "release")


def cli(argv):
    # Returns (stdout, stderr, status).
    if not argv:
        return (HELP, "", 0)
    argv = list(argv)
    versions = []
    ranges = []
    incl = None
    loose = incpre = do_coerce = rtl = reverse = False
    ident = None
    base = None

    def shift():
        return argv.pop(0) if argv else None

    while argv:
        a = argv.pop(0)
        if "=" in a:
            k = a.index("=")
            argv.insert(0, a[k + 1:])
            a = a[:k]
        if a in ("-rv", "-rev", "--rev", "--reverse"):
            reverse = True
        elif a in ("-l", "--loose"):
            loose = True
        elif a in ("-p", "--include-prerelease"):
            incpre = True
        elif a in ("-v", "--version"):
            versions.append(shift())
        elif a in ("-i", "--inc", "--increment"):
            if argv and argv[0] in LEVELS:
                incl = argv.pop(0)
            else:
                incl = "patch"
        elif a == "--preid":
            ident = shift()
        elif a in ("-r", "--range"):
            ranges.append(shift())
        elif a == "-n":
            base = shift()
            if base == "false":
                base = False
        elif a in ("-c", "--coerce"):
            do_coerce = True
        elif a == "--rtl":
            rtl = True
        elif a == "--ltr":
            rtl = False
        elif a in ("-h", "--help", "-?"):
            return (HELP, "", 0)
        else:
            versions.append(a)
    if do_coerce:
        out = []
        for v in versions:
            c = coerce(v, loose, incpre, rtl)
            out.append(c.version if c else v)
        versions = out
    versions = [v for v in versions if v is not None and valid(v)]
    if not versions:
        return ("", "", 1)
    if incl and (len(versions) != 1 or ranges):
        return ("", "--inc can only be used on a single version with no range\n", 1)
    for r in ranges:
        versions = [v for v in versions if satisfies(v, r, loose, incpre)]
        if not versions:
            return ("", "", 1)
    if reverse:
        versions = sort_stable(versions, lambda a, b: compare(b, a, loose, incpre))
    else:
        versions = sort_stable(versions, lambda a, b: compare(a, b, loose, incpre))
    out = ""
    for v in versions:
        c = parse(re.sub(r"^[=v]+", "", js_trim(v)), loose, incpre)
        c = c.version if c else None
        if incl:
            c = inc(c, incl, loose, incpre, ident, base)
        out += ("null" if c is None else c) + "\n"
    return (out, "", 0)


# --- library calls

def show(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    return str(v)


def js_json(xs):
    return "[" + ",".join(str(x) if isinstance(x, int) else json.dumps(x) for x in xs) + "]"


def lib(fn, args):
    loose = incpre = rtl = False
    a = []
    for x in args:
        if x == "--loose":
            loose = True
        elif x == "-p":
            incpre = True
        elif x == "--rtl":
            rtl = True
        else:
            a.append(x)
    try:
        if fn == "parse":
            v = parse(a[0], loose, incpre)
            if not v:
                return "null"
            return "%d %d %d pre=%s build=%s" % (v.major, v.minor, v.patch, js_json(v.prerelease), js_json(v.build))
        if fn == "validRange":
            return show(valid_range(a[0], loose, incpre))
        if fn == "minVersion":
            v = min_version(a[0], loose, incpre)
            return v.version if v else "null"
        if fn == "maxSatisfying":
            return show(max_satisfying(a[1:], a[0], loose, incpre, -1))
        if fn == "minSatisfying":
            return show(max_satisfying(a[1:], a[0], loose, incpre, 1))
        if fn == "intersects":
            return show(intersects(a[0], a[1], loose, incpre))
        if fn == "diff":
            return show(diff(a[0], a[1]))
        if fn == "compareBuild":
            x = SemVer(a[0], loose, incpre)
            y = SemVer(a[1], loose, incpre)
            return show(x.compare(y) or x.compare_build(y))
        if fn == "simplify":
            return show(simplify(a[1:], a[0], loose, incpre))
        if fn == "coerce":
            v = coerce(a[0], loose, incpre, rtl)
            return v.version if v else "null"
        if fn == "inc":
            base = a[3] if len(a) > 3 else None
            if base == "false":
                base = False
            return show(inc(a[0], a[1], loose, incpre, a[2] if len(a) > 2 else None, base))
    except VersionError as e:
        return "error: " + str(e)
    return "unknown function " + fn


# --- outdated

def pick(pk, spec):
    tags = pk.get("dist-tags", {})
    if valid_range(spec) is None:
        return tags[spec] if spec in tags else "INVALID"
    if tags.get("latest") and satisfies(tags["latest"], spec):
        return tags["latest"]
    dep = pk.get("deprecated", {})
    live = [v for v in pk["versions"] if v not in dep]
    return (max_satisfying(live, spec, False, False, -1)
            or max_satisfying(pk["versions"], spec, False, False, -1) or "NONE")


def table(rows):
    w = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    return "\n".join("  ".join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip() for r in rows) + "\n"


def gt(a, b):
    return compare(a, b) > 0


def lt(a, b):
    return compare(a, b) < 0


def outdated(d):
    def load(p):
        with open(p) as f:
            return json.load(f)
    pj = load(os.path.join(DATA, d, "package.json"))
    lock = load(os.path.join(DATA, d, "package-lock.json"))
    reg = load(os.path.join(DATA, "registry.json"))
    deps = []
    for kind in ("dependencies", "devDependencies", "optionalDependencies"):
        for name, spec in pj.get(kind, {}).items():
            deps.append((name, spec, kind))
    deps.sort(key=lambda x: x[0])
    rows = [["Package", "Current", "Wanted", "Latest", "Type"]]
    notes = []
    for name, spec, kind in deps:
        pk = reg.get(name)
        entry = lock.get("packages", {}).get("node_modules/" + name)
        current = entry["version"] if entry else "MISSING"
        if not pk:
            notes.append("%s: not in the registry" % name)
            continue
        wanted = pick(pk, spec)
        latest = pk.get("dist-tags", {}).get("latest") or "NONE"
        if current == wanted and current == latest:
            continue
        rows.append([name, current, wanted, latest, kind])
        if wanted == "INVALID":
            notes.append('%s: "%s" is not a range or a dist-tag' % (name, spec))
            continue
        if wanted == "NONE":
            notes.append('%s: nothing satisfies "%s"' % (name, spec))
            continue
        if current != "MISSING" and valid(current):
            if lt(current, wanted):
                notes.append("%s: %s -> %s (%s)" % (name, current, wanted, diff(current, wanted)))
            elif gt(current, wanted):
                notes.append('%s: %s is newer than "%s" allows; wanted %s' % (name, current, spec, wanted))
            if not satisfies(current, spec) and valid_range(spec) is not None:
                notes.append('%s: installed %s does not satisfy "%s"' % (name, current, spec))
        elif current == "MISSING":
            notes.append("%s: not installed; would install %s" % (name, wanted))
        if valid(wanted) and gt(latest, wanted):
            notes.append('%s: %s is out of range "%s" (%s)' % (name, latest, spec, diff(wanted, latest)))
        dep = pk.get("deprecated", {})
        if current in dep:
            notes.append("%s: %s is deprecated: %s" % (name, current, dep[current]))
    out = table(rows) if len(rows) > 1 else "everything is up to date\n"
    for n in notes:
        out += n + "\n"
    return out


def words(line):
    out = []
    i = 0
    while i < len(line):
        if line[i] == " ":
            i += 1
            continue
        if line[i] == '"':
            j = line.index('"', i + 1)
            out.append(line[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < len(line) and line[j] != " ":
                j += 1
            out.append(line[i:j])
            i = j
    return out


out = []
with open(os.path.join(DATA, "jobs.txt")) as f:
    jobs = f.read().split("\n")
for line in jobs:
    if line == "" or line.startswith("#"):
        continue
    out.append("$ " + line + "\n")
    w = words(line)
    if w[0] == "semver":
        so, se, st = cli(w[1:])
        out.append(so + se)
        if st != 0:
            out.append("[exit status %d]\n" % st)
    elif w[0] == "lib":
        out.append(lib(w[1], w[2:]) + "\n")
    elif w[0] == "outdated":
        out.append(outdated(w[1]))
    out.append("\n")
sys.stdout.write("".join(out))
