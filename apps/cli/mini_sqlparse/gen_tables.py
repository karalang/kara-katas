# Prints the Kara functions that hold sqlparse's lexer table (SQL_REGEX)
# and its keyword dictionaries, read from the package in sqlparse/, for
# mini_sqlparse.kara's table section. Run as `python3 -I gen_tables.py`.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlparse import keywords as K  # noqa: E402


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


print("// sqlparse.keywords.SQL_REGEX: each pattern with the token type it")
print("// gives, or \"\" for PROCESS_AS_KEYWORD (a keyword lookup).")
print("fn sql_regex() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for rx, tt in K.SQL_REGEX:
    t = "" if tt is K.PROCESS_AS_KEYWORD else str(tt)
    print("    v.push((%s.to_string(), %s.to_string()));" % (lit(rx), lit(t)))
print("    v")
print("}")

DICTS = ["KEYWORDS_COMMON", "KEYWORDS_ORACLE", "KEYWORDS_MYSQL", "KEYWORDS_PLPGSQL",
         "KEYWORDS_HQL", "KEYWORDS_MSACCESS", "KEYWORDS_SNOWFLAKE", "KEYWORDS_BIGQUERY",
         "KEYWORDS"]
lines = []
for name in DICTS:
    for k, v in getattr(K, name).items():
        lines.append("    add_kw(mut m, %s, %s);" % (lit(k), lit(str(v))))
chunks = [lines[i:i + 180] for i in range(0, len(lines), 180)]
print()
print("// The keyword dictionaries in the order the default Lexer adds them; the")
print("// first dictionary that holds a word decides its type.")
print("fn keyword_table() -> Map[String, String] {")
print("    let mut m: Map[String, String] = Map.new();")
for k in range(len(chunks)):
    print("    keywords_%d(mut m);" % k)
print("    m")
print("}")
for k, c in enumerate(chunks):
    print()
    print("fn keywords_%d(m: mut ref Map[String, String]) {" % k)
    for line in c:
        print(line)
    print("}")


# The characters a match of each pattern can start with. The lexer tries
# every pattern in order at every position, and most of them cannot start
# with the character there; the Kara side skips those. The sets come from
# the parsed pattern and are a superset of the truth: a pattern that can
# match the empty string, or one this cannot read, may start anywhere.
import re  # noqa: E402
import re._constants as C  # noqa: E402
import re._parser as P  # noqa: E402

FLAGS = re.IGNORECASE | re.UNICODE
ALL = (set(range(128)), True, False)


def cased(c):
    out = {c}
    if c < 128:
        ch = chr(c)
        out |= {ord(ch.lower()), ord(ch.upper())}
    return {x for x in out if x < 128}


def category(cat):
    rx = {C.CATEGORY_DIGIT: r"\d", C.CATEGORY_NOT_DIGIT: r"\D", C.CATEGORY_SPACE: r"\s",
          C.CATEGORY_NOT_SPACE: r"\S", C.CATEGORY_WORD: r"\w", C.CATEGORY_NOT_WORD: r"\W"}[cat]
    return {c for c in range(128) if re.match(rx, chr(c), FLAGS)}


def first_in(items):
    s = set()
    neg = False
    for op, av in items:
        if op is C.NEGATE:
            neg = True
        elif op is C.LITERAL:
            s |= cased(av)
        elif op is C.RANGE:
            for c in range(av[0], min(av[1], 127) + 1):
                s |= cased(c)
        elif op is C.CATEGORY:
            s |= category(av)
        else:
            return set(range(128))
    if neg:
        s = set(range(128)) - s
    return s


def first_seq(seq):
    acc = set()
    nonascii = False
    for op, av in seq:
        s, na, nullable = first_item(op, av)
        acc |= s
        nonascii = nonascii or na
        if not nullable:
            return acc, nonascii, False
    return acc, nonascii, True


def first_item(op, av):
    if op is C.LITERAL:
        letter = av < 128 and chr(av).isalpha()
        return cased(av), av >= 128 or letter, False
    if op is C.NOT_LITERAL:
        return set(range(128)) - cased(av), True, False
    if op is C.IN:
        return first_in(av), True, False
    if op is C.ANY:
        return set(range(128)) - {10}, True, False
    if op is C.SUBPATTERN:
        return first_seq(av[3])
    if op is C.ATOMIC_GROUP:
        return first_seq(av)
    if op is C.BRANCH:
        acc, na, nl = set(), False, False
        for b in av[1]:
            s, n, z = first_seq(b)
            acc |= s
            na = na or n
            nl = nl or z
        return acc, na, nl
    if op in (C.MAX_REPEAT, C.MIN_REPEAT, C.POSSESSIVE_REPEAT):
        s, na, nl = first_seq(av[2])
        return s, na, nl or av[0] == 0
    if op in (C.AT, C.ASSERT, C.ASSERT_NOT):
        return set(), False, True
    return set(range(128)), True, True


def first_of(rx):
    s, na, nullable = first_seq(P.parse(rx, FLAGS))
    if nullable:
        return ALL[0], True
    return s, na


def check_sound(texts):
    for rx, _ in K.SQL_REGEX:
        s, na = first_of(rx)
        m = re.compile(rx, FLAGS).match
        for t in texts:
            for i in range(len(t)):
                if m(t, i):
                    c = ord(t[i])
                    assert (c < 128 and c in s) or (c >= 128 and na), (rx, t[i])


print()
print("// The characters a match of each SQL_REGEX pattern can start with, worked")
print("// out from the parsed pattern by gen_tables.py: one '1' or '0' for each")
print("// ASCII code, then one for every other character.")
print("fn sql_first() -> Vec[String] {")
print("    let mut v: Vec[String] = Vec.new();")
for rx, _ in K.SQL_REGEX:
    s, na = first_of(rx)
    bits = "".join("1" if c in s else "0" for c in range(128)) + ("1" if na else "0")
    print('    v.push("%s".to_string());' % bits)
print("    v")
print("}")
