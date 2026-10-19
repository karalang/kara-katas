# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_validators.kara's data section: each file's path under data/ and, for a binary one, its
# bytes as hex. No function gets more than about 200
# lines.
import os


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def is_text(b):
    if b.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\r\t" for c in s)


names = []
for root, dirs, files in os.walk("data"):
    for f in files:
        names.append(os.path.relpath(os.path.join(root, f), "data"))
names.sort()

# Each file's text is pushed by helpers of at most 180 lines, so no
# function gets long however big the file is.
print("// The files under data/, in path order.")
print("fn data_files() -> Vec[DataFile] {")
print("    let mut v: Vec[DataFile] = Vec.new();")
helpers = []
for k, n in enumerate(names):
    b = open(os.path.join("data", n), "rb").read()
    if is_text(b):
        pieces = [lit(line) for line in b.decode("utf-8").splitlines(keepends=True)]
        hexed = "false"
    else:
        h = b.hex()
        pieces = [lit(h[i:i + 96]) for i in range(0, len(h), 96)]
        hexed = "true"
    print("    let mut t%d = String.new();" % k)
    for j in range(0, len(pieces), 180):
        name = "data_file_%d_%d" % (k, j // 180)
        print("    %s(mut t%d);" % (name, k))
        helpers.append((name, pieces[j:j + 180]))
    print("    v.push(DataFile { path: %s.to_string(), hex: %s, body: t%d });" % (lit(n), hexed, k))
print("    v")
print("}")
for name, body in helpers:
    print()
    print("fn %s(t: mut ref String) {" % name)
    for piece in body:
        print("    t.push_str(%s);" % piece)
    print("}")

# ---------------------------------------------------------------- tables

# The Unicode and country tables the port needs, from this Python and from
# the vendored validators package.
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validators import country  # noqa: E402


def ranges(pred):
    out = []
    start = None
    for cp in range(0x110000):
        ok = pred(chr(cp))
        if ok and start is None:
            start = cp
        elif not ok and start is not None:
            out.append((start, cp - 1))
            start = None
    if start is not None:
        out.append((start, 0x10FFFF))
    return out


def range_fn(name, comment, rs):
    rows = [rs[i:i + 6] for i in range(0, len(rs), 6)]
    parts = [rows[i:i + 150] for i in range(0, len(rows), 150)]
    print()
    print("// " + comment)
    print("fn %s() -> Vec[(i64, i64)] {" % name)
    print("    let mut v: Vec[(i64, i64)] = Vec.new();")
    for k in range(len(parts)):
        print("    %s_%d(mut v);" % (name, k))
    print("    v")
    print("}")
    for k, part in enumerate(parts):
        print()
        print("fn %s_%d(v: mut ref Vec[(i64, i64)]) {" % (name, k))
        for row in part:
            print("    " + " ".join("v.push((0x%X, 0x%X));" % r for r in row))
        print("}")


def set_fn(name, comment, items):
    items = sorted(items)
    print()
    print("// " + comment)
    print("fn %s() -> Vec[String] {" % name)
    print("    let mut v: Vec[String] = Vec.new();")
    for i in range(0, len(items), 8):
        print("    " + " ".join("v.push(%s.to_string());" % lit(x) for x in items[i:i + 8]))
    print("    v")
    print("}")


range_fn("digit_only_ranges", "Characters str.isdigit() accepts that are not decimal digits.",
         ranges(lambda c: c.isdigit() and not c.isdecimal()))
range_fn("alpha_ranges", "Characters str.isalpha() accepts.", ranges(lambda c: c.isalpha()))
range_fn("nfkc_netloc_ranges", "Characters whose NFKC form holds one of / ? # @ :, which urlsplit refuses in a netloc.",
         ranges(lambda c: c not in "/?#@:" and any(x in unicodedata.normalize("NFKC", c) for x in "/?#@:")))
set_fn("alpha2_codes", "country._alpha3_to_alpha2's values.", set(country._alpha3_to_alpha2.values()))
set_fn("alpha3_codes", "country._alpha3_to_alpha2's keys.", set(country._alpha3_to_alpha2))
set_fn("numeric_codes", "country._numeric.", country._numeric)
set_fn("calling_codes", "country._calling_codes's values.", set(country._calling_codes.values()))
set_fn("currency_codes", "country._currency_iso4217.", country._currency_iso4217)
set_fn("currency_symbols", "country._currency_symbols.", country._currency_symbols)

# The regular expressions, as validators writes them.
_ssn_marks = "0123456789ABCDEFHJKLMNPRSTUVWXY"
patterns = [
    ("email", r"(^[Ā-ſƀ-ɏ -ÿ]"
     + r"|[Ā-ſƀ-ɏ -ÿ0-9a-z!#$%&'*+/=?^_`{}|~\-]+"
     + r"(\.[Ā-ſƀ-ɏ -ÿ0-9a-z!#$%&'*+/=?^_`{}|~\-]+)*$"
     + r'|^"('
     + r"[Ā-ſƀ-ɏ -ÿ\001-\010\013\014\016-\037"
     + r"!#-\[\]-\177]|\\[\011.]"
     + r')*")$'),
    ("domain_bad", r"\s|__+"),
    ("port", r"^\:(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|"
     + r"6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3})$"),
    ("simple_host", r"^(?!-)[a-z0-9](?:[a-z0-9-]{0,59}[a-z0-9])?(?<!-)$"),
    ("private_172", r"^172\.(?:1[6-9]|2\d|3[0-1])\."),
    ("broadcast", r"^(?:22[4-9]|23[0-9]|24[0-9]|25[0-5])\."),
    ("url_user", r"(^[Ā-ſƀ-ɏ]"
     + r"|[-!#$%&'*+/=?^_`{}|~0-9a-z]+(\.[-!#$%&'*+/=?^_`{}|~0-9a-z]+)*$"
     + r"|^([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\011.])*$)"),
    ("url_path", r"^[\/a-z0-9\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@\%"
     + r"\U0001F300-\U0001F5FF"
     + r"\U0001F600-\U0001F64F"
     + r" -퟿豈-﷏ﷰ-￯]+$"),
    ("whitespace", r"\s"),
    ("url_fragment", r"[0-9a-z?/:@\-._~%!$&'()*+,;=#]*"),
    ("ipvfuture", r"\A[vV][a-fA-F0-9]+\..+\Z"),
    ("mac", r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"),
    ("slug", r"^[a-z0-9]+(?:-[a-z0-9]+)*$"),
    ("base16", r"^[0-9A-Fa-f]+$"),
    ("base32", r"^[A-Z2-7]+=*$"),
    ("base58", r"^[1-9A-HJ-NP-Za-km-z]+$"),
    ("base64", r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$"),
    ("visa", r"^4"),
    ("mastercard", r"^(5[1-5]|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)"),
    ("amex", r"^(34|37)"),
    ("unionpay", r"^62"),
    ("diners", r"^(30|36|38|39)"),
    ("jcb", r"^35"),
    ("discover", r"^(60|64|65)"),
    ("mir", r"^(220[0-4])"),
    ("iban", r"^[a-z]{2}[0-9]{2}[a-z0-9]{11,30}$"),
    ("btc_segwit", r"^(bc|tb)[0-3][02-9ac-hj-np-z]{14,74}$"),
    ("trx", r"^[T][a-km-zA-HJ-NP-Z1-9]{33}$"),
    ("bsc", r"0x[a-fA-F0-9]{40}"),
    ("fi_business_id", r"^[0-9]{7}-[0-9]$"),
    ("fi_ssn", r"""^
        (?P<date>(0[1-9]|[1-2]\d|3[01])
        (0[1-9]|1[012])
        (\d{{2}}))
        [ABCDEFYXWVU+-]
        (?P<serial>(\d{{3}}))
        (?P<checksum>[{check_marks}])$""".format(check_marks=_ssn_marks)),
    ("fr_ssn", r"^([12])" r"\s(\d{2})" r"\s(0[1-9]|1[0-2])" r"\s(\d{2,3}|2[AB])" r"\s(\d{2,3})"
     r"\s(\d{3})" r"(?:\s(\d{2}))?$"),
    ("aadhar", r"^[2-9]{1}\d{3}\s\d{4}\s\d{4}$"),
    ("pan", r"[A-Z]{5}\d{4}[A-Z]{1}"),
]
for service in ["", "_"]:
    for trailing in [r"$", r"\.?$"]:
        patterns.append(("domain%s%s" % ("_srv" if service else "", "_dot" if trailing != "$" else ""),
                         rf"^(?:[a-z0-9{service}]"
                         + rf"(?:[a-z0-9-{service}]{{0,61}}"
                         + rf"[a-z0-9{service}])?\.)"
                         + r"+[a-z0-9][a-z0-9-]{0,61}"
                         + rf"[a-z]{trailing}"))
for n in [32, 40, 56, 64, 96, 128]:
    patterns.append(("hash%d" % n, r"^[0-9a-f]{%d}$" % n))
print()
print("// The patterns validators compiles, one function each.")
for name, p in patterns:
    print("fn pat_%s() -> String {" % name)
    print("    %s.to_string()" % lit(p))
    print("}")
