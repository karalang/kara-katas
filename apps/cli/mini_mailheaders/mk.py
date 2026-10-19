# Writes data/: a small mailbox under data/mail/ (one message per file)
# and data/jobs.jsonl, the calls mini_mailheaders makes into email.utils
# and email.header before it reads the mailbox.
import json
import os

os.makedirs("data/mail", exist_ok=True)

MAIL = [
    """From: "Ana Lima" <ana.lima@example.org>
To: Ben Okafor <ben@example.net>, "Chen, Wei" <wei.chen@example.com>
Cc: team@example.org
Date: Mon, 19 Oct 2026 09:30:00 -0500
Subject: Quarterly report
Message-ID: <r1@example.org>

Hi all,
""",
    """From: =?utf-8?q?Jos=C3=A9_Mart=C3=ADnez?= <jose@example.es>
To: =?iso-8859-1?q?Fran=E7ois?= <francois@example.fr>
Date: Tue, 20 Oct 2026 14:05:59 +0200
Subject: =?utf-8?b?UmU6IFJldW5pw7NuIGRlbCBsdW5lcw==?=

Hola
""",
    """From: =?UTF-8?B?5bGx55Sw5aSq6YOO?= <yamada@example.jp>
To: undisclosed-recipients:;
Date: 21 Oct 2026 08:00 +0900
Subject: =?UTF-8?B?5Lya6K2w44Gu6K2w5LqL6Yyy?=
 =?UTF-8?B?44Gr44Gk44GE44Gm?=

本文
""",
    """From: billing@example.com (Example Billing)
To: "O'Brien, Pat" <pat.obrien@example.ie>
Date: Wed, 21 Oct 2026 23:59:60 +0000
Subject: Your invoice =?windows-1252?q?=80_42?= is ready

Invoice
""",
    """From: Grüße Team <gruesse@example.de>
To: Dörte <doerte@example.de>
Date: Thu, 22 Oct 26 10:15:00 CEST
Subject: Grüße aus Köln

Hallo
""",
    """From: "Support \\"Desk\\"" <support@example.com>
Reply-To: <help@example.com>
To: alice@example.com, bob@example.com,
  carol@example.com
Date: Fri, 23 Oct 2026 07:00:00 -0000
Subject: [Ticket #4411] Printer on 3rd floor

Fixed.
""",
    """From: Eve <eve@example.com>
To: "Mallory" <mallory@example.com>, a@b@c.example
Cc: Trent <trent@[192.0.2.1]>
Date: Sat, 24 Oct 2026 12:00:00 EDT
Subject: =?iso-8859-15?q?Prix_=A4_10?= =?utf-8?q?_=E2=82=AC?=

Test
""",
    """From: news@example.org
To: list@example.org (Weekly list)
Date: Sunday, 25-Oct-26 06:30:00 GMT
Subject: =?utf-8?q?Weekly_digest_=E2=80=94_issue_?= 42
 =?utf-8?q?=E2=9C=93?=

Digest
""",
    """From: Dana Scully <dana@example.gov>
To: Fox Mulder <fox@example.gov>
Date: Mon, 26 Oct 2026 25:00:00 +0000
Subject: =?us-ascii?q?Truth_is_out_there?=

?
""",
    """From: =?utf-8?b?QmFkIGJhc2U2NA?= <bad@example.com>
To: <x@example.com>
Date: not a date
Subject: =?utf-8?b?///?=

x
""",
    """From: Résumé Bot <bot@example.com>
To: hr@example.com
Date: Tue, 27 Oct 2026 16:45:12 +0530
Subject: =?x-unknown?q?Mystery?=

x
""",
]
for i, m in enumerate(MAIL):
    with open(f"data/mail/{i + 1:02d}.eml", "w", encoding="utf-8") as f:
        f.write(m)

jobs = []


def J(fn, *args, **kw):
    jobs.append({"fn": fn, "args": list(args), "kw": kw})


ADDRS = [
    "alice@example.com", "Alice <alice@example.com>", '"Alice Smith" <alice@example.com>',
    "alice@example.com (Alice Smith)", "Alice Smith <alice@example.com> (work)", "<alice@example.com>",
    '"Smith, Alice" <alice@example.com>', "Smith, Alice <alice@example.com>", '"a\\"b" <x@y.z>',
    "alice", "alice@", "@example.com", "a@b@c.example", "Trent <trent@[192.0.2.1]>",
    "user@[IPv6:2001:db8::1]", "a.b.c@example.com", "a . b @ example . com", '"a b"@example.com',
    "José <jose@example.es>", "=?utf-8?q?Jos=C3=A9?= <jose@example.es>", "Group: a@x.y, b@x.y;",
    "undisclosed-recipients:;", "(only a comment)", "Bob (x(y)z) <bob@example.com>",
    "Bob (unclosed <bob@example.com>", "Bob ) <bob@example.com>", "", "   ", "a@x.y, b@x.y",
    "<@route.example:a@x.y>", "Joe <joe @ example . com>", "Name\n <name@example.com>",
    '"quoted, comma" <q@example.com>, other@example.com', "a@x.y,,b@x.y", "Al <al@x.y", "Al al@x.y>",
    "\"unterminated <u@x.y>", "a@x.y; b@x.y", "Mr. Smith <smith@x.y>", "Dr. J. R. R. Tolkien <jrr@x.y>",
]
for a in ADDRS:
    J("parseaddr", a)
    J("parseaddr", a, strict=False)
GROUPS = [
    ["alice@example.com, Bob <bob@example.com>"],
    ["alice@example.com", "Bob <bob@example.com>"],
    ['"Smith, Alice" <alice@example.com>', "carol@example.com"],
    ["Smith, Alice <alice@example.com>"],
    ["Group: a@x.y, b@x.y;", "c@x.y"],
    ["Bob (x <bob@example.com>", "c@x.y"],
    ["a@b@c.example, d@e.f"],
    ["Trent <trent@[192.0.2.1]>, ok@x.y"],
    ["", "a@x.y"],
    ["a@x.y,", "b@x.y"],
    ["undisclosed-recipients:;"],
    ['"a, b" <c@d.e>, "f, g" <h@i.j>'],
    ['"a\\", b" <c@d.e>'],
]
for g in GROUPS:
    J("getaddresses", g)
    J("getaddresses", g, strict=False)
for pair, cs in [(("", "a@x.y"), None), (("Alice", "a@x.y"), None), (("Smith, Alice", "a@x.y"), None),
                 (('Al "the pal"', "a@x.y"), None), (("José", "j@x.y"), None), (("José", "j@x.y"), "iso-8859-1"),
                 (("山田太郎", "y@x.jp"), None), (("Zoë Ångström-Øster", "z@x.y"), None), (("a\\b", "a@x.y"), None),
                 (("Ab", "jösé@x.y"), None), (("€uro", "e@x.y"), "iso-8859-1"), (("€uro", "e@x.y"), "iso-8859-15"),
                 (("€uro", "e@x.y"), "windows-1252"), (("x" * 30 + "é", "e@x.y"), None), (("éééééééé", "e@x.y"), None),
                 (("Dr. Who", "who@x.y"), None), (("a@b", "c@d"), None), (("[ops]", "o@x.y"), None),
                 (("José", "j@x.y"), "latin-1"), (("José", "j@x.y"), "koi8-zz")]:
    J("formataddr", list(pair), **({} if cs is None else {"charset": cs}))
for s in ['say "hi"', "back\\slash", "plain", ""]:
    J("quote", s)
for s in ['"quoted"', '"esc \\"q\\" \\\\ x"', "<angle>", '"', "<", '"half', "<a>b>", "x"]:
    J("unquote", s)
DATES = [
    "Mon, 19 Oct 2026 09:30:00 -0500", "Tue, 20 Oct 2026 14:05:59 +0200", "21 Oct 2026 08:00 +0900",
    "Wed, 21 Oct 2026 23:59:60 +0000", "Thu, 22 Oct 26 10:15:00 CEST", "Fri, 23 Oct 2026 07:00:00 -0000",
    "Sat, 24 Oct 2026 12:00:00 EDT", "Sunday, 25-Oct-26 06:30:00 GMT", "Mon, 26 Oct 2026 25:00:00 +0000",
    "not a date", "", "   ", "Mon,19 Oct 2026 09:30:00 -0500", "19 October 2026 09:30:00 +0100",
    "Oct 19 2026 09:30:00 PST", "19 Oct 2026 09.30.15 +0100", "19 Oct 2026 09.30 +0100", "19 Oct 69 00:00 Z",
    "19 Oct 68 00:00 UT", "19 Oct 2026 9:5:7 +0000", "19 Oct 2026 09:30:00+0200", "19 Oct 2026 09:30:00-0730",
    "19 Oct 2026 09:30:00 +05:30", "19 Oct 2026 09:30:00 +2500", "19 Oct 2026 09:30:00 -2500",
    "32 Oct 2026 09:30:00 +0000", "29 Feb 2026 00:00:00 +0000", "29 Feb 2024 00:00:00 +0000",
    "19 Foo 2026 09:30:00 +0000", "Oct 19, 2026 09:30:00 +0000", "19 Oct 2026, 09:30:00 +0000",
    "19 Oct 2026 09:30:00, +0000", "19 Oct 2026 09:30:00 +0000 (UTC)", "19 Oct 0 00:00:00 +0000",
    "19 Oct 10000 00:00:00 +0000", "19 Oct 2_026 09:30:00 +0000", "19 Oct 2026 09:61:00 +0000",
    "Mon 19 Oct 2026 09:30:00 +0000", "monday, 19 oct 2026 09:30:00 +0000", "19 Oct 2026 09:30:00 MSK",
    "19 Oct 2026 09:30:00 -0", "19 Oct 2026 09:30:00 +0", "19 Oct 2026 09:30:00 +12345", "19 Oct 2026",
    "19 Oct 2026 09:30:00:00 +0000", "x, 19 Oct 2026 09:30:00 +0000", "19-Oct-2026 09:30:00 +0000",
]
for d in DATES:
    J("parsedate_tz", d)
    J("parsedate", d)
    J("parsedate_to_datetime", d)
    J("mktime_tz", d)
for t, gmt in [(0, False), (0, True), (1792414200, False), (1792414200, True), (1792414200.9999996, False),
               (1792414200.4999995, True), (-1, False), (-0.5, True), (951782400, False), (253402300799, True),
               (1e9, False)]:
    J("formatdate", t, usegmt=gmt)
for s in ["us-ascii'en'This%20is", "utf-8''%E2%82%AC%20rates", "no-ticks", "one'tick", "a'b'c'd", "''"]:
    J("decode_rfc2231", s)
for s, cs, lang in [("This is ~ fine", None, None), ("€ rates", "utf-8", None), ("café", "iso-8859-1", "fr"),
                    ("a/b c", None, "en"), ("€", "iso-8859-1", None), ("€", "ascii", None)]:
    kw = {}
    if cs is not None:
        kw["charset"] = cs
    if lang is not None:
        kw["language"] = lang
    J("encode_rfc2231", s, **kw)
for v in ["plain", '"quoted"', ["utf-8", "", "%E2%82%AC"], ["iso-8859-1", "fr", "caf%E9"], ["", "", "abc"],
          ["utf-8", "", "\\xff"], ["no-such-codec", "", '"x"'], ["us-ascii", "", "café"]]:
    J("collapse_rfc2231_value", v)
SUBJECTS = [
    "Plain subject", "=?utf-8?q?Jos=C3=A9?=", "=?UTF-8?B?5bGx55Sw5aSq6YOO?=",
    "=?utf-8?q?a?= =?utf-8?q?b?=", "=?utf-8?q?a?=  \t =?utf-8?q?b?=", "=?utf-8?q?a?= x =?utf-8?q?b?=",
    "pre =?utf-8?q?mid?= post", "=?iso-8859-1?q?caf=E9?= =?utf-8?q?_ok?=", "  leading =?utf-8?q?x?=",
    "=?utf-8?b?UmU6IFJldW5pw7NuIGRlbCBsdW5lcw==?=", "=?utf-8?b?UmU6IFJldW5pw7NuIGRlbCBsdW5lcw?=",
    "=?utf-8?b?QmFkIGJhc2U2NA?=", "=?utf-8?b?///?=", "=?utf-8?b?Z===?=", "=?utf-8?Q?under_score=5F?=",
    "=?utf-8?q?=e2=82=ac?=", "=?utf-8?q?=E2=82=AC?=", "=?utf-8?q?=ZZ?=", "=?utf-8?x?nope?=",
    "=?utf-8?q??=", "=??q?nocharset?=", "Grüße =?utf-8?q?aus?= Köln", "日本 =?utf-8?q?x?=",
    "=?utf-8?q?café?=", "=?utf-8?q?€?=", "=?iso-8859-15?q?Prix_=A4_10?= =?utf-8?q?_=E2=82=AC?=",
    "=?utf-8?q?Weekly_digest_=E2=80=94_issue_?= 42\n =?utf-8?q?=E2=9C=93?=",
    "=?UTF-8?B?5Lya6K2w44Gu6K2w5LqL6Yyy?=\n =?UTF-8?B?44Gr44Gk44GE44Gm?=", "=?x-unknown?q?Mystery?=",
    "=?utf-8?q?bad=FF?=", "=?us-ascii?q?caf=E9?=", "=?windows-1252?q?=80_42?=", "=?utf-8?q?trunc=E2=82?=",
    "=?utf-8*en?q?lang?=", "=?utf-8?q?a?b?=",
]
for s in SUBJECTS:
    J("decode_header", s)
    J("str_make_header", s)
    J("encode_make_header", s)
HEADERS = [
    ({"s": "Hello world"}, {}),
    ({"s": "Hello wörld"}, {}),
    ({"s": "Hello wörld", "charset": "utf-8"}, {}),
    ({"s": "Hello wörld", "charset": "iso-8859-1"}, {}),
    ({"s": "€ 10", "charset": "iso-8859-1"}, {}),
    ({"s": "€ 10", "charset": "windows-1252"}, {}),
    ({"s": "a" * 100}, {}),
    ({"s": " ".join(["word%d" % i for i in range(30)]), "header_name": "Subject"}, {}),
    ({"s": "; ".join(["key%d=value%d" % (i, i) for i in range(12)]), "header_name": "Content-Type"}, {}),
    ({"s": ", ".join(["user%d@example.com" % i for i in range(9)]), "header_name": "To"}, {}),
    ({"s": ", ".join(["user%d@example.com" % i for i in range(9)]), "header_name": "To"}, {"splitchars": " "}),
    ({"s": "Grüße aus Köln und München, " * 4, "charset": "utf-8", "header_name": "Subject"}, {}),
    ({"s": "日本語のテキスト" * 6, "charset": "utf-8", "header_name": "Subject"}, {}),
    ({"s": "Résumé of the café meeting", "charset": "iso-8859-1", "header_name": "Subject"}, {}),
    ({"s": "x" * 70, "header_name": "X-Long-Header-Name"}, {}),
    ({"s": "short", "maxlinelen": 10}, {}),
    ({"s": "Grüße aus Köln", "charset": "utf-8", "maxlinelen": 30}, {}),
    ({"s": "Grüße aus Köln", "charset": "utf-8"}, {"maxlinelen": 0}),
    ({"s": "line one\nline two\n  indented three"}, {}),
    ({"s": "line one\nBcc: injected@example.com"}, {}),
    ({"s": "Grüße\nKöln", "charset": "utf-8"}, {}),
    ({"s": "tab\tseparated\twords " * 5, "header_name": "Subject"}, {}),
    ({"s": "a, b", "continuation_ws": "\t", "header_name": "To", "maxlinelen": 8}, {}),
    ({"s": "Hello", "charset": "us-ascii"}, {"linesep": "\r\n"}),
    ({"s": "Hello wörld", "charset": "ascii"}, {}),
    ({"s": "naïve", "charset": "koi8-zz"}, {}),
    ({"s": "", "charset": "utf-8"}, {}),
    ({"s": "x", "charset": "Latin_1"}, {}),
]
for kw, enc in HEADERS:
    J("header", **{"init": kw, "encode": enc})
PARTS = [
    [["Hello ", None], ["wörld", "utf-8"], [" again", None]],
    [["Price: ", "us-ascii"], ["10 €", "iso-8859-15"], ["(", None], ["net", "utf-8"], [")", None]],
    [["a", "utf-8"], ["b", "utf-8"], ["c", "iso-8859-1"], ["d", "iso-8859-1"]],
    [["café", "us-ascii"], ["ok", None]],
    [["€", "iso-8859-1"]],
]
for p in PARTS:
    J("header_parts", p)

with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs))
