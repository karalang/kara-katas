# Writes data/: the jobs mini_email_validator runs (data/jobs.jsonl), the
# DNS answers its resolver serves (data/dns.tsv), a newsletter's sign-up
# log (data/signups.tsv), idna's tables for the characters the jobs can
# reach (data/uts46.txt, data/idnadata.txt), and what Python's unicodedata
# (Unicode 15.1 in Python 3.13) says about them (data/unicode.txt).
#
# The address cases are email-validator's own test inputs, read from
# ev_tests/test_syntax.py with a stand-in for pytest that only records
# the parameter lists, plus the cases written below. Everything is fixed,
# so the files never change.
import bisect
import json
import os
import re
import shutil
import sys
import types
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "mini_idna"))
from idna import idnadata  # noqa: E402
from idna.uts46data import uts46_replacements, uts46_starts, uts46_statuses  # noqa: E402

DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)

# ------------------------------------------------------------ upstream inputs

recorded = []


def parametrize(names, values, **kw):
    recorded.append(values)
    return lambda f: f


fake = types.ModuleType("pytest")
fake.mark = types.SimpleNamespace(parametrize=parametrize)
fake.raises = None
fake.MonkeyPatch = object
fake.CaptureFixture = {str: object}
sys.modules["pytest"] = fake
import ev_tests.test_syntax  # noqa: E402,F401
del sys.modules["pytest"]


def first(v):
    return v[0] if isinstance(v, (tuple, list)) else v


def has_surrogate(s):
    return any(0xD800 <= ord(c) < 0xE000 for c in s)


upstream = []
for values in recorded:
    for v in values:
        s = first(v)
        if not has_surrogate(s) and s not in upstream:
            upstream.append(s)
# test_email_unsafe_character builds its addresses from fragments.
unsafe = []
for values in recorded:
    for v in values:
        if isinstance(v, tuple) and len(v) == 2 and "@" not in v[0] and len(v[0]) < 25:
            unsafe.append(v[0])

jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def val(email, **opts):
    return {"op": "validate", "email": email, "opts": opts}


NO_DNS = {"check_deliverability": False}

job("upstream inputs, defaults without DNS", [val(s, **NO_DNS) for s in upstream])
job("upstream inputs, ASCII only", [val(s, allow_smtputf8=False, check_deliverability=False) for s in upstream])
job("upstream inputs, every option on, test environment",
    [val(s, allow_quoted_local=True, allow_domain_literal=True, allow_display_name=True,
         allow_empty_local=True, test_environment=True) for s in upstream])
job("unsafe characters", [val(s + "@test", test_environment=True) for s in unsafe if not has_surrogate(s)]
    + [val("test@" + s, test_environment=True) for s in unsafe if not has_surrogate(s)])

# ------------------------------------------------------------ more corners

job("as the README shows them", [
    {"op": "show", "email": "test@joshdata.me", "opts": NO_DNS},
    {"op": "show", "email": "jeff@臺網中心.tw", "opts": NO_DNS},
    {"op": "show", "email": "ñoñó@example.com", "opts": NO_DNS},
    {"op": "show", "email": "\"quoted local\"@example.com", "opts": {"allow_quoted_local": True, "check_deliverability": False}},
    {"op": "show", "email": "Jane Doe <jane@example.com>", "opts": {"allow_display_name": True, "check_deliverability": False}},
    {"op": "show", "email": "ops@[192.0.2.10]", "opts": {"allow_domain_literal": True}},
    {"op": "show", "email": "ops@[IPv6:2001:DB8:0:0:0:0:0:1]", "opts": {"allow_domain_literal": True}},
    {"op": "show", "email": "Postmaster@example.com", "opts": NO_DNS},
    {"op": "show", "email": "ana@shop.example", "opts": {}},
    {"op": "show", "email": "ana@fallback.example", "opts": {}},
])

corners = [
    # display names
    "\"Doe, Jane\" <jane@example.com>",
    "\"Jane \\\"JD\\\" Doe\" <jane@example.com>",
    "Jane <jane@example.com>>>",
    "Jane <jane@example.com>   ",
    "Jane　<jane@example.com>",
    "Jane\t <jane@example.com>",
    "Jáne <jane@example.com>",
    "Jane ​<jane@example.com>",
    "<>",
    "Jane <>",
    "Jane <@example.com>",
    "\"unterminated <jane@example.com>",
    "\"Jane\"x <jane@example.com>",
    "\"Jane\"éあ <jane@example.com>",
    "Jane <\"q\"@example.com>",
    "a@b <c@example.com>",
    # quoted local parts
    "\"\"@example.com",
    "\"a\\\"b\"@example.com",
    "\"a\\\\b\"@example.com",
    "\"tab\there\"@example.com",
    "\"é́\"@example.com",
    "\"x\"y@example.com",
    "\"cr\rlf\"@example.com",
    "\" \"@example.com",
    "\" \"@example.com",
    "\"\"@example.com",
    "\"POSTMASTER\"@example.com",
    "\"Abuse\"@example.com",
    # NFC and the special characters
    "a̸@example.com",
    "≮@example.com",
    "a@̸example.com",
    "é@example.com",
    "Å@example.com",
    "ẛ̣@example.com",
    "ﬁx@example.com",
    "￿@example.com",
    "\U000e0001@example.com",
    "x@é.example",
    "x@É.example",
    "x@İstanbul.example",
    "x@straße.example",
    "x@xn--strae-oqa.example",
    "x@XN--BCHER-KVA.example",
    "x@xn--bcher-kva.example",
    "x@bücher.example",
    "x@xn--zca.example",
    "x@xn--abc.example",
    "x@xn--a.example",
    "x@ab--cd.example",
    "x@xn--.example",
    "x@ＡＢＣ.example",
    "x@a。b．c｡example",
    "x@⒈.example",
    "x@­.example",
    "x@a­b.example",
    "x@‍.example",
    "x@a‌b.example",
    "x@אב.example",
    "x@אa.example",
    "x@1א.example",
    "x@١۱.example",
    "x@・.example",
    "x@a・ア.example",
    "x@กา.example",
    "x@̀a.example",
    "x@a.123",
    "x@a.c0m",
    "x@a.c-m",
    "x@.",
    "x@..",
    "x@-",
    "x@a-.b",
    "x@a.-b",
    "x@a_b.example",
    "x@[]",
    "x@[1.2.3]",
    "x@[1.2.3.04]",
    "x@[1.2.3.4.5]",
    "x@[1..3.4]",
    "x@[1.2.3.4\n]",
    "x@[0x7f.0.0.1]",
    "x@[IPv6:]",
    "x@[IPv6:fe80::1%eth0]",
    "x@[IPv6:fe80::1%]",
    "x@[IPv6:::ffff:192.0.2.1]",
    "x@[IPv6:1:2:3:4:5:6:7:8:9]",
    "x@[IPv6:1::2::3]",
    "x@[IPv6:12345::]",
    "x@[IPv6:1:2:3:4:5:6:7::]",
    "x@[ipv6:::1]",
    "x@[IPv4:1.2.3.4]",
    "x@[tag:û]",
    "x@[tag:ü]",
    "x@[1.2.3.4]x",
    "x@[1.2.3.4",
    # lengths
    "a" * 64 + "@example.com",
    "é" * 64 + "@example.com",
    "é" * 32 + "@example.com",
    "é" * 33 + "@example.com",
    "x@" + "a" * 63 + ".example",
    "x@" + "é" * 59 + ".example",
    "x@" + ".".join(["a" * 63] * 3) + "." + "b" * 61,
    "x@" + ".".join(["a" * 63] * 3) + "." + "b" * 62,
    "x@" + ".".join(["é" * 20] * 9) + ".example",
    "xyz" * 20 + "@" + ".".join(["b" * 60] * 3) + ".example",
    "\U0001f600" * 10 + "@" + ".".join(["b" * 60] * 3) + ".example",
    "\U0001f600" * 10 + "@" + ".".join(["b" * 60] * 3) + "." + "c" * 7,
    # whitespace and controls
    " x@example.com",
    "x@example.com ",
    "x @example.com",
    "x@ example.com",
    "x\x00@example.com",
    "x@exa\x7fmple.com",
    "x\u0085@example.com",
    # special-use names
    "x@a.arpa", "x@onion", "x@a.onion", "x@test", "x@a.test", "x@LOCALHOST", "x@a.local",
    "x@a.invalid", "x@example", "x@example.example",
]
job("corners, defaults without DNS", [val(s, **NO_DNS) for s in corners])
job("corners, every option on", [val(s, allow_quoted_local=True, allow_domain_literal=True,
                                     allow_display_name=True, allow_empty_local=True,
                                     check_deliverability=False) for s in corners])
job("corners, ASCII only, not globally deliverable",
    [val(s, allow_smtputf8=False, globally_deliverable=False, check_deliverability=False) for s in corners])
job("corners, test environment", [val(s, test_environment=True) for s in corners])

job("bytes", [
    {"op": "validate", "bytes": "jane@example.com".encode().hex(), "opts": NO_DNS},
    {"op": "validate", "bytes": "jáne@example.com".encode().hex(), "opts": NO_DNS},
    {"op": "validate", "bytes": "jane@xn--bcher-kva.example".encode().hex(), "opts": NO_DNS},
    {"op": "validate", "bytes": "jane@bücher.example".encode("latin-1").hex(), "opts": NO_DNS},
    {"op": "validate", "bytes": "", "opts": NO_DNS},
])

# ------------------------------------------------------------ the DNS

# name, type, value. NXDOMAIN, TIMEOUT, NONAMESERVERS and YXDOMAIN as a
# type make every query for the name fail that way; a name with no row
# at all does not exist.
DNS = [
    ("example.com", "MX", "10 mx1.example.com."),
    ("example.com", "MX", "20 mx2.example.com."),
    ("example.com", "MX", "10 MX0.Example.COM."),
    ("example.net", "MX", "0 ."),
    ("example.org", "MX", "0 ."),
    ("example.org", "MX", "10 mx.example.org."),
    ("shop.example", "MX", "5 aspmx.mail.example."),
    ("shop.example", "MX", "10 alt1.aspmx.mail.example."),
    ("shop.example", "TXT", "\"v=spf1 -all\""),
    ("fallback.example", "A", "192.0.2.80"),
    ("fallback.example", "A", "198.51.100.25"),
    ("fallback.example", "A", "203.0.113.9"),
    ("fallback.example", "A", "93.184.216.34"),
    ("fallback.example", "TXT", "\"v=spf1 a\" \" -all\""),
    ("v6only.example", "AAAA", "2a00:1450:4001:80b::200e"),
    ("v6only.example", "TXT", "\"google-site-verification=abc\""),
    ("private.example", "A", "10.0.0.5"),
    ("private.example", "A", "192.168.1.1"),
    ("private.example", "AAAA", "fd00::25"),
    ("private.example", "AAAA", "::1"),
    ("loopback.example", "A", "127.0.0.1"),
    ("cgnat.example", "A", "100.64.0.7"),
    ("cgnat.example", "AAAA", "2001:db8::25"),
    ("mapped.example", "AAAA", "::ffff:93.184.216.34"),
    ("noreply.example", "A", "93.184.216.34"),
    ("noreply.example", "TXT", "\"v=spf1\" \" -all\""),
    ("noreply.example", "TXT", "\"some other text\""),
    ("nosend.example", "A", "93.184.216.34"),
    ("nosend.example", "TXT", "\"v=spf1 -all \""),
    ("nosend.example", "TXT", "\"v=spf1 include:_spf.example.net -all\""),
    ("nosend2.example", "A", "93.184.216.34"),
    ("nosend2.example", "TXT", "\"v=spf1 -all\""),
    ("txtonly.example", "TXT", "\"hello\""),
    ("mail.example", "A", "198.51.100.30"),
    ("aspmx.mail.example", "A", "198.51.100.31"),
    ("slow.example", "TIMEOUT", ""),
    ("broken.example", "NONAMESERVERS", ""),
    ("dname.example", "YXDOMAIN", ""),
    ("gone.example", "NXDOMAIN", ""),
    ("xn--bcher-kva.example", "MX", "10 mx.xn--bcher-kva.example."),
    ("xn--r8jz45g.example", "MX", "10 mail.xn--r8jz45g.example."),
    ("xn--fiqq24b10vi0d.tw", "MX", "10 mx.twnic.example."),
    ("xn--mnchen-3ya.example", "A", "203.0.113.50"),
    ("mixed.example", "MX", "30 c.example."),
    ("mixed.example", "MX", "10 b.example."),
    ("mixed.example", "MX", "10 a.example."),
    ("mixed.example", "MX", "0 ."),
    ("upper.example", "MX", "10 MX.UPPER.EXAMPLE."),
]

with open(os.path.join(DATA, "dns.tsv"), "w") as f:
    f.write("# name\ttype\tvalue (the text form of the record)\n")
    for row in DNS:
        f.write("\t".join(row) + "\n")

domains = sorted({r[0] for r in DNS}) + ["nowhere.example", "com.example", "mx1.example.com"]
job("deliverability", [val("someone@" + d) for d in domains]
    + [val("someone@" + d, allow_smtputf8=False) for d in ("bücher.example", "例え.example", "münchen.example")]
    + [val("someone@BÜCHER.example"), val("someone@shop.example", timeout=5),
       val("someone@shop.example", test_environment=True), val("someone@[192.0.2.1]", allow_domain_literal=True),
       val("someone@slow.example", check_deliverability=False)])

# ------------------------------------------------------------ the command line


def cli(args, env=None, stdin=None):
    return {"op": "cli", "args": args, "env": env or {}, "stdin": stdin or []}


job("python -m email_validator", [
    cli(["test@example.com"]),
    cli(["test@shop.example"]),
    cli(["test@fallback.example"]),
    cli(["test@slow.example"]),
    cli(["test@gone.example"]),
    cli(["Jane <jane@example.com>"]),
    cli(["Jane <jane@example.com>"], {"ALLOW_DISPLAY_NAME": "1"}),
    cli(["\"Doe, Jane\" <jane@example.com>"], {"CHECK_DELIVERABILITY": ""}),
    cli(["ops@[IPv6:2001:db8::1]"], {"ALLOW_DOMAIN_LITERAL": "yes"}),
    cli(["ops@[IPv6:fe80::1%eth0]"], {"ALLOW_DOMAIN_LITERAL": "0"}),
    cli(["\"q\\\"t\"@bücher.example"], {"ALLOW_QUOTED_LOCAL": "1"}),
    cli(["ñoñó@bücher.example"]),
    cli(["ñoñó@bücher.example"], {"ALLOW_SMTPUTF8": ""}),
    cli(["x@a.test"], {"TEST_ENVIRONMENT": "1"}),
    cli(["x@intranet"], {"GLOBALLY_DELIVERABLE": "", "CHECK_DELIVERABILITY": ""}),
    cli(["x@example.com"], {"DEFAULT_TIMEOUT": "5"}),
    cli(["control\x01@example.com"]),
    cli([], {}, ["good@example.com", "  padded@example.com　", "bad@", "no-mx@example.net",
                 "dead@gone.example", "é@example.com", "", "two@@example.com", "x@slow.example",
                 "x@broken.example", "x@dname.example"]),
    cli([], {"ALLOW_SMTPUTF8": "", "CHECK_DELIVERABILITY": ""}, ["é@example.com", "e@é.example", "a@b.c"]),
    cli([], {"DEFAULT_TIMEOUT": "1"}, ["good@example.com"]),
    cli(["a@example.com", "ignored"]),
])

# ------------------------------------------------------------ sign-ups

SIGNUPS = [
    ("2026-10-01T09:12", "web", "Ana Lima", "ana.lima@example.com"),
    ("2026-10-01T09:15", "web", "Ben Ode", "Ben.Ode+news@Example.COM"),
    ("2026-10-01T09:20", "web", "ana again", "ana.lima@EXAMPLE.com"),
    ("2026-10-01T09:31", "web", "Chloé", "chloé@shop.example"),
    ("2026-10-01T10:02", "web", "", "POSTMASTER@example.com"),
    ("2026-10-01T10:03", "web", "", "postmaster@example.com"),
    ("2026-10-01T10:40", "mime", "", "\"Dana Kim\" <dana@fallback.example>"),
    ("2026-10-01T10:41", "mime", "Dana K.", "Dana <dana@fallback.example>"),
    ("2026-10-01T11:00", "web", "Eli", "eli@gmial.con"),
    ("2026-10-01T11:01", "web", "Eli", "eli@gone.example"),
    ("2026-10-01T11:02", "web", "Eli", "eli@example.net"),
    ("2026-10-01T11:05", "web", "Eli", "eli@v6only.example"),
    ("2026-10-02T08:00", "web", "Fatma", "fatma@bücher.example"),
    ("2026-10-02T08:01", "web", "Fatma (copy)", "fatma@xn--bcher-kva.example"),
    ("2026-10-02T08:05", "web", "Gō", "go@例え.example"),
    ("2026-10-02T08:07", "web", "Hana", "はな@例え.example"),
    ("2026-10-02T09:30", "web", "Ivan", "ivan@private.example"),
    ("2026-10-02T09:31", "web", "Ivan", "ivan@noreply.example"),
    ("2026-10-02T09:32", "web", "Ivan", "ivan@nosend.example"),
    ("2026-10-02T09:33", "web", "Ivan", "ivan@nosend2.example"),
    ("2026-10-02T09:40", "web", "Jo", "jo@slow.example"),
    ("2026-10-02T09:41", "web", "Jo", "jo@broken.example"),
    ("2026-10-02T09:42", "web", "Jo", "jo@dname.example"),
    ("2026-10-02T09:43", "web", "Jo", "jo@txtonly.example"),
    ("2026-10-02T12:00", "legacy", "Kai", "\"kai smith\"@example.com"),
    ("2026-10-02T12:01", "legacy", "Kai", "\"kai.smith\"@example.com"),
    ("2026-10-02T12:02", "legacy", "Kai", "kai.smith@example.com"),
    ("2026-10-02T12:03", "legacy", "Lee", "lee@[192.0.2.44]"),
    ("2026-10-02T12:04", "legacy", "Lee", "lee@[IPv6:2001:DB8::44]"),
    ("2026-10-02T12:05", "legacy", "Lee", "lee@[IPv6:2001:db8:0::44]"),
    ("2026-10-02T12:06", "legacy", "Mo", "mo@intranet"),
    ("2026-10-02T12:07", "web", "Mo", "mo@intranet"),
    ("2026-10-03T07:00", "web", "Noor", " noor@example.org"),
    ("2026-10-03T07:01", "web", "Noor", "noor@example.org"),
    ("2026-10-03T07:02", "web", "Noor", "noor@mixed.example"),
    ("2026-10-03T07:03", "web", "Omar", "omar@upper.example"),
    ("2026-10-03T07:04", "web", "Omar", "omar@münchen.example"),
    ("2026-10-03T07:05", "web", "Pia", "pia@cgnat.example"),
    ("2026-10-03T07:06", "web", "Pia", "pia@mapped.example"),
    ("2026-10-03T07:07", "web", "Pia", "pia@loopback.example"),
    ("2026-10-03T07:08", "web", "Quinn", "émile@example.com"),
    ("2026-10-03T07:09", "web", "Quinn", "émile@example.com"),
    ("2026-10-03T07:10", "web", "Ray", "ray@shop.example."),
    ("2026-10-03T07:11", "web", "Ray", "ray@shop..example"),
    ("2026-10-03T07:12", "web", "Ray", "ray@localhost"),
    ("2026-10-03T07:13", "web", "Ray", "ray@a.local"),
    ("2026-10-03T07:14", "mime", "", "Ray Q <ray@shop.example> (work)"),
    ("2026-10-03T07:15", "mime", "", "\"Ray Q\" <\"ray q\"@shop.example>"),
]
with open(os.path.join(DATA, "signups.tsv"), "w") as f:
    f.write("# when\tform\tname\taddress\n")
    for row in SIGNUPS:
        f.write("\t".join(row) + "\n")
job("newsletter sign-ups", [{"op": "signups"}])

with open(os.path.join(DATA, "jobs.jsonl"), "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")

# ------------------------------------------------------------ the tables

DOTS = "[.。．｡]"


def row(cp):
    return cp if cp < 256 else bisect.bisect_right(uts46_starts, cp) - 1


covered = set(range(0x80))
strings = []
for j in jobs:
    for op in j["ops"]:
        if "email" in op:
            strings.append(op["email"])
        if "bytes" in op:
            strings.append(bytes.fromhex(op["bytes"]).decode("latin-1"))
        strings.extend(op.get("args", []))
        strings.extend(op.get("stdin", []))
for r in SIGNUPS:
    strings.extend(r)
for r in DNS:
    strings.extend(r)
for s in strings:
    covered.update(ord(c) for c in s)


def punycode_chars(s):
    out = set()
    # labels of a domain, wherever it sits in an address
    for label in re.split(r"[.。．｡@<>\[\] \t]", s):
        b = label.lower()
        if b.startswith("xn--") and b.isascii():
            try:
                out.update(ord(c) for c in b[4:].encode().decode("punycode"))
            except Exception:
                pass
    return out


for s in strings:
    covered |= punycode_chars(s)
    covered |= punycode_chars("".join(uts46_replacements[row(ord(c))] or c for c in s))


def decomp(cp):
    d = unicodedata.decomposition(chr(cp))
    if not d or d.startswith("<"):
        return []
    return [int(x, 16) for x in d.split()]


composites = {}
for cp in range(0x110000):
    if 0xD800 <= cp < 0xE000:
        continue
    d = decomp(cp)
    if len(d) == 2 and unicodedata.normalize("NFC", chr(cp)) == chr(cp):
        composites.setdefault(d[0], []).append((d[1], cp))
for li in range(19):
    for vi in range(21):
        lv = 0xAC00 + (li * 21 + vi) * 28
        composites.setdefault(0x1100 + li, []).append((0x1161 + vi, lv))
        for ti in range(1, 28):
            composites.setdefault(lv, []).append((0x11A7 + ti, lv + ti))

while True:
    more = set()
    for cp in covered:
        rep = uts46_replacements[row(cp)]
        if rep:
            more.update(ord(c) for c in rep)
        more.update(decomp(cp))
        for second, comp in composites.get(cp, []):
            if second in covered:
                more.add(comp)
    more -= covered
    if not more:
        break
    covered |= more

with open(os.path.join(DATA, "unicode.txt"), "w") as f:
    f.write("# cp;ccc;canonical decomposition;flags (p not printable, n no name, c primary composite);"
            "bidi;category;name (for the categories email-validator names)\n")
    for cp in sorted(covered):
        ch = chr(cp)
        d = decomp(cp)
        flags = ("p" if not ch.isprintable() else "") + ("n" if not unicodedata.name(ch, "") else "")
        if len(d) == 2 and unicodedata.normalize("NFC", ch) == ch:
            flags += "c"
        cat = unicodedata.category(ch)
        name = "" if cat[0] in "LNPS" else unicodedata.name(ch, "")
        f.write("%x;%d;%s;%s;%s;%s;%s\n" % (cp, unicodedata.combining(ch), " ".join("%x" % x for x in d), flags,
                                            unicodedata.bidirectional(ch), cat, name))

rows = sorted({row(cp) for cp in covered})
with open(os.path.join(DATA, "uts46.txt"), "w") as f:
    f.write("# start;status;replacement\n")
    for i in rows:
        rep = uts46_replacements[i]
        f.write("%x;%s;%s\n" % (uts46_starts[i], chr(uts46_statuses[i]),
                                " ".join("%x" % ord(c) for c in rep) if rep else ""))


def ranges(name, rs):
    return ["%s %x %x" % (name, r >> 32, r & 0xFFFFFFFF) for r in rs]


with open(os.path.join(DATA, "idnadata.txt"), "w") as f:
    f.write("# set start end (end exclusive)\n")
    for k, v in idnadata.codepoint_classes.items():
        f.write("\n".join(ranges(k, v)) + "\n")
    for k, v in idnadata.scripts.items():
        f.write("\n".join(ranges("script:" + k, v)) + "\n")
    for k, v in idnadata.joining_types.items():
        f.write("\n".join(ranges("joining:" + k, v)) + "\n")

print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations,", len(covered), "characters,",
      len(rows), "UTS #46 rows")
