"""Writes data/jobs.txt and the documents in data/docs/ that the jobs read.

A job line is `grammar<TAB>mode<TAB>input`. An input that starts with @
names a file in data/docs/; any other input is the text itself, with
backslash escapes for a newline, tab, carriage return and backslash and
\\x{hex} for any other character outside printable ASCII.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BS = chr(92)


def esc(s):
    out = []
    for c in s:
        if c == BS:
            out.append(BS + BS)
        elif c == "\n":
            out.append(BS + "n")
        elif c == "\t":
            out.append(BS + "t")
        elif c == "\r":
            out.append(BS + "r")
        elif " " <= c <= "~":
            out.append(c)
        else:
            out.append(BS + "x{%x}" % ord(c))
    return "".join(out)


JOBS = []


def job(name, mode, *inputs):
    for text in inputs:
        JOBS.append(f"{name}\t{mode}\t{text if text.startswith('@') else esc(text)}")


def parse(name, *inputs):
    job(name, "parse", *inputs)


def partial(name, *inputs):
    job(name, "partial", *inputs)


def tokens(name, *specs):
    for spec in specs:
        JOBS.append(f"{name}\ttokens\t{spec}")


# ------------------------------------------------------------ parsy's tests
parse("string", "x", "y", "", "xx")
parse("string_lower", "x", "X", "y")
parse("string_cat", "cat", "CAT", "CaT", "dog", "Ca")
parse("regex_digit", "1", "4", "x", "")
parse("regex_group", "a1b", "x", "a12b")
parse("regex_name", "a1b", "x")
parse("regex_tuple", "a1b2c", "x", "a1b2")
parse("regex_optional_group", "12.5", "12", "12.")
partial("regex_optional_group", "12.", "3.14.15")
parse("regex_flags", "SELECT name", "select  id", "Select", "update x")
parse("then", "xy", "y", "z", "x")
parse("bind", "xy", "x", "xz")
parse("bind_double", "aa", "ab", "zz", "1")
parse("map", "7", "x")
parse("combine", "1A", "A1")
parse("combine_dict_date", "05042003", "29022024", "0504200")
parse("combine_dict_pair", "ABC123", "ABC", "abc123")
parse("combine_dict_none", "ABC   123", "ABC123")
parse("combine_dict_underscore", "ABC   123", "ABC \t\n 7")
parse("concat", "", "abc", "ab1")
parse("generate", "xy", "x", "yx")
parse("generate_parser", "xy", "xx")
parse("mark", "asdf\nqwer\n", "a\n\nbc\n", "ab\ncd")
parse("tag", "this,is,a,list", "", "one,,two")
parse("tag_dict", "Hello", "H", "")
parse("generate_desc", "t", "x")
parse("generate_no_desc", "ab", "ax", "")
parse("abc", "a", "b", "c", "d", "")
parse("backtrack", "z", "xq", "w")
parse("or", "x", "y", "z")
parse("or_then", BS + "y", "z", BS + "z", BS)
parse("many", "x", "xyz", "", "1", "ab1")
parse("many_then", "y", "xy", "xxxxxy", "xxx")
parse("times0", "", "x")
parse("times3", "xyz", "xy", "xyzw")
parse("times3_then", "xyz1", "xy1", "xyz", "xyzw")
parse("times2_4", "xy", "xyz", "xyzw", "x", "xyzwv")
parse("times2_4_then", "xy1", "xyz1", "xyzw1", "xy", "xyzw", "xyzwv1", "x1")
parse("at_most", "", "ab", "abab", "ababab", "aba")
parse("at_least", "abab", "ababab", "ab", "")
partial("until", "ssssx", "ssssxy", "xxx", "ssssy", "xssssxy")
parse("until", "ssssy", "xssssxy")
parse("until_seq", "ssssx")
partial("until_seq", "ssssxy")
parse("until_then", "ssssx")
partial("until_then", "ssssxy")
partial("until_any", "xxxx", "abcx", "abc")
parse("until_consume", "ssssx", "ssssy", "xssssxy")
partial("until_consume", "ssssxy", "xxx")
partial("until_min", "sssx", "sssssx", "ssx", "x")
partial("until_max", "ssx", "sssx", "ssssx", "x")
partial("until_min_max", "sssx", "sssssx", "ssx", "ssssssx")
parse("optional", "a", "", "b")
parse("optional_b", "a", "", "aa")
parse("sep_by", "1,2,3,4", "9,0,4,7", "3,7", "8", "", "8,", ",9", "82", "7.6")
parse("sep_by_2_4", "1,2,3,4", "3,7", "8", "", "8,", ",9", "82", "7.6", "1,2,3,4,5")
parse("sep_by_max0", "", "1")
parse("add", "a1", "ab", "1a")
parse("add_lists", "ab1", "ab123", "ab1234", "a1")
parse("multiply", "abc", "ab", "abcd")
parse("multiply_range", "a", "ab", "abc", "")
parse("alt_empty", "", "a")
parse("alt", "a", "1", ".")
parse("seq_empty", "", "a")
parse("seq1", "a", "1")
parse("seq2", "a1", "1a", "a")
parse("seq_kw", "Jane Smith", "Jane", "Jane  Smith  ")
parse("seq_kw_a", "a", "b")
parse("ascii", "a", chr(0x263A), "", "~")
parse("char_from", "a", "b", "x", "ab")
parse("titles", "Mr", "Mr.", "Mrs", "Mrs.", "foo", "M")
parse("titles_hyde", "Mr. Hyde", "Mrs Hyde", "Mr  Hyde")
parse("titles_lower", "mr", "mr.", "MR", "MR.", "mRS.", "ms")
partial("peek_any", "abc", "")
parse("peek_digit", "a", "1", "")
parse("any_char", "x", "\n", "", chr(0x4E2D))
parse("whitespace", "\n", " ", " \t\r\n\x0b\x0c", "x", chr(0x3000) + chr(0xA0))
parse("letter", "a", "1", chr(0xE9), chr(0x3A9), chr(0x4E2D), "_")
parse("digit", chr(0xB9), "2", "x", chr(0x663), chr(0x2460), chr(0xBD))
parse("decimal", "9876543210", chr(0xB9), chr(0x663) + "1", "12a")
parse("line_info", "AB\nCD", "\n\nx", "")
tokens("index", "A|B", "A|B|C|D", "")
parse("index", "abc", "ab1")
parse("should_fail", "a", "abc", "a10", "", "8", "8ab")
parse("should_fail_value", "")
parse("enum_pet", "cat", "dog", "foo", "caterpillar", "Cat")
parse("enum_position", "1", "2", "12", "3")
parse("enum_pet_lower", "cat", "CAT", "Dog", "CATERPILLAR")
parse("eof", "a", "ab", "")
tokens("start_stop", "START", "STOP", "START|hello", "START|STOP|START", "")
tokens("match_start", "START", "", "STOP")
tokens("match_start_default", "x", "y")
parse("match_start_default", "x", "y")
tokens("bracketed", "START|hello|#1|#2|goodbye|STOP", "START|STOP", "START|hello", "hello|STOP", "START|STOP|STOP")
parse("forward", "(0 1 (2 3))", "7", "()", "(1 (2 (3 (4))))", "(1  2)", "(1 2")
parse("forward_az", "Z", "AZ", "AAAAAZ", "A", "B")
partial("forward_az", "AAZXX")
parse("forward_unset", "()")
partial("forward_unset", "()")
JOBS.append("forward_unset\tbecome_twice\t")
for text, idx in [("abc\ndef", 0), ("abc\ndef", 2), ("abc\ndef", 3), ("abc\ndef", 4), ("abc\ndef", 7), ("abc\ndef", 8), ("\n\n", 2), ("", 0)]:
    JOBS.append(f"line_info\tlineinfo\t{esc(text)} {idx}")

# ------------------------------------------------------------ parsy's examples
parse(
    "json",
    "{\n    \"int\": 1,\n    \"string\": \"hello\",\n    \"a list\": [1, 2, 3],\n    \"escapes\": \"\\n "
    + BS
    + "u24D2\",\n    \"nested\": {\"x\": \"y\"},\n    \"other\": [true, false, null]\n}\n",
    "[]",
    "  {}  ",
    "[1.5, -0.25, 1e3, 2E-2, 0, -0]",
    "{\"a\": [1, 2,]}",
    "{\"a\" 1}",
    "\"unterminated",
    "[\"" + BS + "\"" + BS + BS + BS + "/" + BS + "b" + BS + "f" + BS + "r" + BS + "t\"]",
    "[\"caf" + BS + "u00e9\", \"" + BS + "u4e2d" + BS + "u6587\"]",
    "[\"bad " + BS + "q escape\"]",
    "{\"dup\": 1, \"dup\": 2}",
    "[[[[[]]]]]",
    "tru",
    "01",
)
parse("json", "@api_response.json", "@package.json", "@broken.json", "@deep.json")
parse(
    "sexpr",
    "(1 2 3)",
    "'foo '(bar baz)",
    "''foo",
    "#t #f",
    "\n            ; a program with a comment\n            (           foo ; that's a foo\n            bar )\n            ; some comments at the end\n            ",
    "(define (square x) (* x x))",
    "(1 2",
    ")",
    "",
)
parse("sexpr", "@config.scm")
parse(
    "select",
    "SELECT thing, stuff, 123, 'hello' FROM my_table WHERE id = 1;",
    "SELECT 1 FROM x;",
    "SELECT name,email FROM users WHERE age >= 21 ;",
    "SELECT a FROM t WHERE b <= -5;",
    "SELECT a FROM t WHERE 'x' < y;",
    "SELECT FROM t;",
    "SELECT a FROM t WHERE b != 1;",
    "SELECT a, FROM t;",
    "select a from t;",
    "SELECT 'it''s' FROM t;",
)
job("logo", "pipe", "fd 1\nbk 2\nrt 90\n", "  fd 10\n  lt 45 \nfd 3", "@square.logo", "fd x\n", "fd 1\nup 2\n", "fd 1 bk 2\n")
job(
    "eval",
    "pipe",
    "1 + 2",
    "2 * (3 + 4)",
    "7 / 2",
    "1 / 3",
    "-3 + +4",
    "10 - 2 - 3",
    "2 * 3.5 - .5",
    "((1))",
    "1 +",
    "(1 + 2",
    "1 2",
    "4 / 8 * 2 + 0.125",
    "1 $ 2",
)

# ------------------------------------------------------------ real-world parsers
parse("ini", "@settings.ini", "@service.conf", "@bad_section.ini", "@bad_line.ini", "", "a=1", "[s]\n", "[ s ] \nk : v ; note\n")
job("access_log", "lines", "@access.log")
parse(
    "csv",
    "@report.csv",
    "@crlf.csv",
    "a,b\n1,2",
    "a,b\n1,2\n",
    "",
    "\"x\"y\"",
    "\"open",
    "a,\"b\nc\",d",
    ",,\n,",
)
parse("http_request", "@get.http", "@post.http", "@folded.http", "@no_blank.http", "GET / HTTP/1.1\r\n\r\n", "GET  / HTTP/1.1\r\n\r\n", "get /x HTTP/2.0\r\n\r\n", "GET /x HTTP/1\r\n\r\n")
parse(
    "semver_range",
    ">=1.2.3 <2.0.0",
    "^1.2.3 || ~2.4",
    "1.x",
    "1.2.3 - 2.3.4",
    "*",
    "=1.0.0-beta.2",
    ">= 1.2 <=1.9 || 3",
    "  ^0.0.1  ",
    ">=01.2",
    "1.2.3 -",
    "",
    "~1.2.3-rc.1 || >2 <3 || 4.x.x",
)
job(
    "query",
    "pipe",
    "status:open",
    "status:open AND owner:bob",
    "status:open owner:bob OR priority>2",
    "NOT (label:\"needs review\" OR label:wip) -draft",
    "title:\"disk full\" AND (host:db-1 OR host:db-2) AND age<=30",
    "printer jam",
    "(a OR b",
    "status:",
    "AND x",
    "size>=-5 NOT NOT x",
    "owner:alice @mention",
    "",
)

DOCS = {}


def doc(name, text):
    DOCS[name] = text


doc(
    "api_response.json",
    """{
  "id": "evt_1Q9xK2",
  "type": "invoice.paid",
  "created": 1729814400,
  "livemode": false,
  "data": {
    "object": {
      "amount_due": 4250,
      "amount_paid": 4250,
      "currency": "eur",
      "customer_name": "Zo""" + BS + """u00eb Ma""" + BS + """u00eftre",
      "discount": null,
      "lines": [
        {"description": "Pro plan \\u00d7 2", "amount": 3800, "tax_rate": 0.19},
        {"description": "Extra seat", "amount": 450, "tax_rate": 0.19}
      ],
      "metadata": {"order": "A-1043", "note": "Thanks! \\"Rush\\" shipping\\n"},
      "paid": true
    }
  },
  "request": {"id": null, "idempotency_key": "6b7f1d2e-1c9a-4d1a-9f2e-3a4b5c6d7e8f"}
}
""".replace("\\u00d7", BS + "u00d7"),
)
doc(
    "package.json",
    """{
  "name": "kitchen-display",
  "version": "2.4.1",
  "private": true,
  "scripts": {
    "build": "tsc -p .",
    "test": "node --test test/",
    "lint": "eslint src/ --max-warnings=0"
  },
  "engines": {"node": ">=20.11"},
  "dependencies": {
    "fastify": "^4.28.1",
    "pino": "~9.3.2",
    "zod": "3.23.8"
  },
  "files": ["dist/", "README.md"],
  "workspaces": []
}
""",
)
doc(
    "broken.json",
    """{
  "name": "orders-api",
  "replicas": 3,
  "env": {
    "PORT": "8080",
    "LOG_LEVEL": "info"
    "REGION": "eu-west-1"
  }
}
""",
)
doc("deep.json", "[" * 12 + "1, [2.5, \"three\"]" + "]" * 12 + "\n")
doc(
    "config.scm",
    """; build configuration for the firmware
(project blinky
  (version 3 1)
  (target 'cortex-m4)
  (debug #f)
  ; flags passed to the compiler
  (flags (opt 2) (warn all) (lto #t))
  (sources 'main 'led 'timer))
""",
)
doc("square.logo", "fd 100\nrt 90\nfd 100\nrt 90\nfd 100\nrt 90\nfd 100\nrt 90\n")
doc(
    "settings.ini",
    """# kitchen display service
name = kitchen-display
debug: false

[server]
host = 0.0.0.0
port = 8080   ; the public port
banner = "Welcome; please wait"  # quoted

[database]
url = postgres://kds:kds@db.internal:5432/kds
pool.size = 10
  timeout = 2.5

; trailing comment
""",
)
doc("service.conf", "[unit]\r\ndescription = orders worker\r\nafter = network.target\r\n\r\n[service]\r\nrestart: on-failure\r\n")
doc("bad_section.ini", "name = x\n\n[server\nport = 1\n")
doc("bad_line.ini", "[server]\nhost = a\nport\n")
doc(
    "access.log",
    '203.0.113.7 - - [09/Mar/2024:17:42:05 +0000] "GET /menu HTTP/1.1" 200 5120 "-" "curl/8.5.0"\n'
    '198.51.100.23 - ana [09/Mar/2024:17:42:06 +0000] "POST /orders HTTP/1.1" 201 312 "https://cafe.example/menu" "Mozilla/5.0 (X11; Linux x86_64)"\n'
    '192.0.2.44 - - [09/Mar/2024:17:42:09 +0100] "GET /static/app.js HTTP/2.0" 304 - "https://cafe.example/" "Mozilla/5.0 \\"quoted\\""\n'
    '203.0.113.9 - - [10/Mar/2024:00:00:01 +0000] "\\x16\\x03\\x01" 400 157 "-" "-"\n'
    '203.0.113.9 - - [10/Foo/2024:00:00:01 +0000] "GET / HTTP/1.1" 200 1 "-" "-"\n'
    '10.0.0.5 - bob [31/Dec/2024:23:59:59 -0500] "DELETE /orders/1043 HTTP/1.1" 204 0 "-" "kds-cli/2.4"\n'
    '10.0.0.5 - bob [31/Dec/2024:23:59:59 -0500] "GET / HTTP/1.1" 999 0 "-" "x"\n',
)
doc(
    "report.csv",
    'region,quarter,revenue,note\nnorth,Q1,1200,\nsouth,Q1,980,"late, but closed"\neast,Q2,1525,"said ""final"""\nwest,Q2,0,"multi\nline"\n',
)
doc("crlf.csv", "id,name\r\n1,Ada\r\n2,\"Grace\r\nHopper\"\r\n")
doc(
    "get.http",
    "GET /api/orders?status=open&limit=20 HTTP/1.1\r\nHost: kds.example\r\nAccept: application/json\r\nUser-Agent: kds-cli/2.4  \r\nX-Request-Id:7f3a\r\n\r\n",
)
doc(
    "post.http",
    "POST /api/orders HTTP/1.1\r\nHost: kds.example\r\nContent-Type: application/json\r\nContent-Length: 27\r\nAuthorization: Bearer test-token-not-real\r\n\r\n",
)
doc("folded.http", "GET / HTTP/1.1\r\nHost: kds.example\r\nX-Long: part one\r\n part two\r\n\r\n")
doc("no_blank.http", "GET / HTTP/1.1\r\nHost: kds.example\r\n")


def main():
    os.makedirs(os.path.join(HERE, "data", "docs"), exist_ok=True)
    with open(os.path.join(HERE, "data", "jobs.txt"), "w", encoding="utf-8") as f:
        for j in JOBS:
            assert "\n" not in j
            f.write(j + "\n")
    for name, text in DOCS.items():
        with open(os.path.join(HERE, "data", "docs", name), "w", encoding="utf-8", newline="") as f:
            f.write(text)
    print(f"{len(JOBS)} jobs, {len(DOCS)} documents")


main()
