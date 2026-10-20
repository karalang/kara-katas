# Writes data/: Hjson and JSON files as people write them (service
# configs, a package manifest, translations, CI settings), files that
# test each corner of the syntax, broken files for each error, and
# jobs.tsv, the jobs oracle.py and mini_hjson.kara run.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, text, newline="\n", bom=False):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = text.replace("\n", newline).encode("utf-8")
    if bom:
        body = b"\xef\xbb\xbf" + body
    with open(path, "wb") as f:
        f.write(body)


SERVICE = """\
# billing-api: settings for every environment
// edit with care; the deploy job reads this file

name: billing-api
version: 2.4.1
owner: payments-team@example.com
listen:
{
  host: 0.0.0.0
  port: 8443
  # TLS terminates at the load balancer
  tls: false
}
database:
{
  url: postgres://billing@db.internal:5432/billing
  pool: 20
  timeout: 2.50
  replicas: [
    db-replica-1.internal
    db-replica-2.internal
  ]
}
/* retry policy, shared with the
   invoice worker */
retry: { attempts: 5, backoff: 1.5e2, jitter: 0.25 }
features:
{
  new-checkout: true
  legacy-invoices: false
  beta-users: null
}
motd:
  '''
  Scheduled maintenance on Sunday.
    Payments may be delayed.
  '''
path: C:\\billing\\data
greeting: hello, world # not a comment inside a quoteless string? it is
rate: 1/3 of traffic
"quoted key with spaces": yes
emptyString: ""
"""

TRANSLATIONS = """\
{
  // UI strings for the checkout page
  "en": {
    title: Checkout
    total: Total: {amount}
    note: '''
      Prices include VAT.
      Shipping is calculated at the next step.
      '''
  },
  "de": {
    title: Kasse
    total: "Summe: {amount}"
    note: Preise inkl. MwSt.
  },
  "ja": {
    title: お会計
    total: 合計: {amount}
  },
  "ar": {
    title: "الدفع"
  }
}
"""

CI = """\
stages: [ "build", "test", "deploy" ]
build:
{
  image: rust:1.80
  script: [
    cargo build --release
    "cargo test -- --nocapture"
  ]
  cache:
  {
    key: cargo-$CI_COMMIT_REF_SLUG
    paths: [
      target/
    ]
  }
}
deploy:
{
  only: [
    main
  ]
  when: manual
  environment: production
  retries: 0
  timeout: 3600
}
"""

PACKAGE_JSON = """\
{
  "name": "@acme/widgets",
  "version": "1.0.0-beta.3",
  "private": true,
  "scripts": {
    "build": "tsc -p .",
    "test": "jest --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "lodash": "~4.17.21"
  },
  "engines": {"node": ">=18"},
  "files": [],
  "config": {}
}
"""

NUMBERS = """\
{
  zero: 0
  negzero: -0
  int: 42
  negative: -17
  big: 123456789012345678901234567890
  onepointzero: 1.0
  trailing: 1.50
  exp: 1e5
  smallexp: 2.5E-3
  tenbillion: 1e10
  justunder: 9999999999.0
  overten: 12345678901.0
  tiny: -1e-7
  zerofrac: 0.000
  negzerofrac: -0.0
  huge: 1e400
  scaled: 3.0e2
  decimals: 0.1
  money: 19.99
  spaced: 7
  notnumber: 1.
  alsonot: 01
  hexish: 0x1F
  plus: +5
  dash: -
  unit: 12px
  version: 1.2.3
  inarray: [1, 2.0, 3e0, -4.50, 5]
}
"""

STRINGS = """\
{
  plain: hello world
  quoted: "hello world"
  single: 'it\\'s'
  singleq: 'say "hi"'
  doubleq: "it's"
  escapes: "tab\\tnew\\nline \\"quote\\" back\\\\slash \\/slash"
  unicode: "caf\\u00e9 \\u263a"
  pair: "\\ud83d\\ude00 grin"
  raw: grüße aus köln
  hashlike: "#not a comment"
  slashy: "// nor this"
  colon: a:b:c
  bracey: "{braces}"
  leading: "  padded  "
  trailingspace: "tail "
  keyword: "true"
  keywordish: true story
  numberish: "42"
  numberish2: 42 apples
  nullish: null pointer
  empty: ""
  quotes: "\\"quoted\\""
  ctrl: "bell\\u0007"
  ls: "line\\u2028sep"
  bom: "\\ufeffmark"
  apos: don't
  url: https://example.com/a?b=c#frag
  comma: "a, b"
  "": empty key
  "a b": spaced key
  "x:y": colon key
  "it's": apostrophe key
}
"""

MULTILINE = """\
text:
  '''
  first line
    indented line

  after a blank line
  '''
oneline: '''just one line'''
quoted: '''has 'single' quotes'''
nested:
{
  poem:
    '''
    Roses are red,
    Violets are blue.
    '''
  inlist: [
    '''
    alpha
    beta
    '''
    plain
  ]
}
"""

DUPES = """\
color: red
size: 1
color: blue
nested: { a: 1, b: 2, a: 3 }
"""

ARRAYS = """\
[
  1
  2, 3,
  [
    nested
    [ "deeper" ]
  ]
  { a: 1 }
  {}
  []
  "",
  last
]
"""

COMMENTS_ONLY = """\
# just a comment
// and another
/* and a block */
"""

ROOT_STRING = "just some text\n"
ROOT_NUMBER = "42\n"
ROOT_QUOTED = "\"a string\"\n"
EMPTY = ""
WS = "   \n\t\n"

BROKEN = {
    "unterminated.hjson": 'a: "never closed\n',
    "badescape.hjson": 'a: "bad \\q escape"\n',
    "badunicode.hjson": 'a: "\\u12g4"\n',
    "shortunicode.hjson": 'a: "\\u12"\n',
    "hexunicode.hjson": 'a: "\\u0x41"\n',
    "control.hjson": 'a: "tab\there"\n',
    "nocolon.hjson": 'a 1\nb: 2\n',
    "keyspace.hjson": 'my key: 1\n',
    "keybrace.hjson": 'a{b: 1\n',
    "emptykey.hjson": ': 1\n',
    "punct.hjson": 'a: ,\n',
    "unclosed.hjson": '[1, 2\n',
    "extra.hjson": '{ a: 1 } b\n',
    "extra2.hjson": '[1] [2]\n',
    "eofkey.hjson": 'a: 1\nb\n',
    "openblock.hjson": 'a: 1 /* never closed\n',
    "slashstar.hjson": 'a: 1\n/*',
    "badml.hjson": "a: '''never closed\n",
    "mlnonewline.hjson": "'''abc'''",
    "valueeof.hjson": "a:",
    "unclosedobj.hjson": "{ a: 1\n",
    "closebracket.hjson": "a: ]\n",
    "colonafter.hjson": "{ \"a\" 1 }\n",
    "inlinelist.hjson": "stages: [ build, test, deploy ]\n",
    "inlineobj.hjson": "cache: { key: cargo, paths: [ target/ ] }\n",
    "triplequotes.hjson": "two_quotes: '''ends with ''''''\n",
}


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    put("service.hjson", SERVICE)
    put("translations.hjson", TRANSLATIONS)
    put("ci.hjson", CI)
    put("package.json", PACKAGE_JSON)
    put("numbers.hjson", NUMBERS)
    put("strings.hjson", STRINGS)
    put("multiline.hjson", MULTILINE)
    put("multiline_crlf.hjson", MULTILINE, newline="\r\n")
    put("bom.hjson", CI, bom=True)
    put("dupes.hjson", DUPES)
    put("arrays.hjson", ARRAYS)
    put("comments.hjson", COMMENTS_ONLY)
    put("rootstring.hjson", ROOT_STRING)
    put("rootnumber.hjson", ROOT_NUMBER)
    put("rootquoted.hjson", ROOT_QUOTED)
    put("empty.hjson", EMPTY)
    put("ws.hjson", WS)
    braced = {}
    for name, text in BROKEN.items():
        put("broken/" + name, text)
        if text[:1] not in "{[":
            # Without braces a bad root object falls back to a quoteless
            # string; inside braces the real error shows.
            braced["braced_" + name] = "{\n" + text + "}\n"
    for name, text in braced.items():
        put("broken/" + name, text)
    BROKEN.update(braced)
    good = ["service.hjson", "translations.hjson", "ci.hjson", "package.json", "numbers.hjson",
            "strings.hjson", "multiline.hjson", "multiline_crlf.hjson", "bom.hjson", "dupes.hjson",
            "arrays.hjson", "comments.hjson", "rootstring.hjson", "rootnumber.hjson",
            "rootquoted.hjson", "empty.hjson", "ws.hjson"]
    jobs = []
    for g in good:
        jobs.append(["hjson", g])
        jobs.append(["hjson", "-j", g])
        jobs.append(["hjson", "-c", g])
    for name in sorted(BROKEN):
        jobs.append(["hjson", "broken/" + name])
    jobs += [
        ["hjson", "-h"],
        ["hjson", "--version"],
        ["hjson", "-x", "ci.hjson"],
        ["hjson", "ci.hjson", "service.hjson"],
        ["dumps", "service.hjson", "sort_keys"],
        ["dumps", "strings.hjson", "ensure_ascii"],
        ["dumps", "translations.hjson", "ensure_ascii"],
        ["dumps", "ci.hjson", "indent=4"],
        ["dumps", "multiline.hjson", "indent=4"],
        ["dumps", "numbers.hjson", "json", "sort_keys"],
        ["dumps", "strings.hjson", "json", "ensure_ascii"],
        ["dumps", "service.hjson", "json", "indent=3"],
        ["dumps", "translations.hjson", "json", "indent=0"],
        ["dumps", "ci.hjson", "json"],
    ]
    for g in good:
        jobs.append(["roundtrip", g])
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
