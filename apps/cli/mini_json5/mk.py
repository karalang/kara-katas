# Writes data/: JSON5 files as real projects keep them (a Renovate
# config, a pnpm package.json5, Chromium-style feature lists, a Babel
# config, a device inventory), files that use every corner of the
# grammar, broken files, one-line cases from json5's own tests, and
# data/jobs.tsv, the jobs that mini_json5.kara and oracle.py run.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FILES = {}

FILES["config/renovate.json5"] = """\
{
  $schema: 'https://docs.renovatebot.com/renovate-schema.json',
  extends: [
    'config:recommended',
    ':semanticCommits',
    'group:allNonMajor', // one PR for the minor bumps
  ],
  timezone: 'Europe/Berlin',
  schedule: ['before 6am on monday'],
  labels: ['dependencies'],
  prConcurrentLimit: 5,
  prHourlyLimit: 0,
  packageRules: [
    {
      matchDepTypes: ['devDependencies'],
      automerge: true,
      automergeType: 'branch',
    },
    {
      // keep the database driver on the 4.x line until the migration
      matchPackageNames: ['pg'],
      allowedVersions: '<5.0.0',
    },
    {
      matchUpdateTypes: ['major'],
      dependencyDashboardApproval: true,
      minimumReleaseAge: '3 days',
    },
  ],
  vulnerabilityAlerts: {
    labels: ['security'],
    assignees: ['@example-org/platform'],
  },
}
"""

FILES["config/package.json5"] = """\
// package.json5, as pnpm reads it
{
  name: '@example/web-console',
  version: '2.14.0',
  private: true,
  description: "The operator's console for the fleet API",
  type: 'module',
  engines: {node: '>=20.11'},
  packageManager: 'pnpm@9.12.0',
  scripts: {
    dev: 'vite --port 5173',
    build: 'tsc -b && vite build',
    test: 'vitest run --coverage',
    'lint:css': 'stylelint "src/**/*.css"',
  },
  dependencies: {
    react: '^18.3.1',
    'react-dom': '^18.3.1',
    zod: '^3.23.8',
  },
  devDependencies: {
    typescript: '~5.6.2',
    vite: '^5.4.8',
    vitest: '^2.1.2',
  },
  pnpm: {
    overrides: {
      'braces@<3.0.3': '>=3.0.3',
    },
  },
}
"""

FILES["config/runtime_enabled_features.json5"] = """\
{
  // Feature flags in the shape a browser engine keeps them: each entry
  // names a feature, its status, and the features it depends on.
  parameters: {
    // "stable" features are on for everyone, "experimental" ones behind
    // a command-line switch, "test" ones only in the test runner.
    status: {
      valid_values: ["stable", "experimental", "test"],
    },
    depends_on: {},
    origin_trial_feature_name: {},
    public: {
      valid_type: "bool",
    },
  },

  data: [
    {
      name: "AccessibilityObjectModel",
      status: "experimental",
    },
    {
      name: "CSSAnchorPositioning",
      status: "stable",
      public: true,
    },
    {
      name: "CSSScrollTimeline",
      status: "experimental",
      depends_on: ["ScrollTimeline"],
      origin_trial_feature_name: "ScrollTimeline",
    },
    {
      name: "FencedFrames",
      status: {"Android": "", "default": "stable"},
    },
    {
      name: "ScrollTimeline",
      status: "test",
    },
  ],
}
"""

FILES["config/babel.config.json5"] = """\
/* Babel config: the presets run last to first. */
{
  presets: [
    ['@babel/preset-env', {
      targets: '> 0.5%, last 2 versions, not dead',
      useBuiltIns: 'usage',
      corejs: 3.38,
    }],
    '@babel/preset-typescript',
  ],
  plugins: [
    ['@babel/plugin-proposal-decorators', {version: '2023-11'}],
  ],
  env: {
    test: {plugins: ['babel-plugin-istanbul']},
  },
  ignore: ['**/*.d.ts', 'dist/**',],
}
"""

FILES["config/inventory.json5"] = """\
// Device inventory, edited by hand in the field.
{
  site: 'Rotterdam DC-2',
  updated: '2026-10-19T07:42:00Z',
  racks: [
    {
      id: 'R14',
      units: 42,
      power_kw: 7.5,
      pdu_load: [.62, .58, 0.7, 1.],
      devices: [
        {host: 'edge-r14-01', serial: 0x5A3F00C2, mac: '3c:ec:ef:12:9a:01', role: 'router',},
        {host: 'stor-r14-07', serial: 0X00ff00ff, disks: 24, raw_tb: 1.92e2,},
      ],
    },
    {
      id: "R15",
      units: 48,
      power_kw: +11,
      pdu_load: [],
      devices: [],
      notes: 'decommission after the \\
Q4 audit',
    },
  ],
  limits: {
    max_temp_c: 27.,
    min_temp_c: -0,
    alarm_after_s: 3E2,
    budget: Infinity,
    drift: -Infinity,
    reading: NaN,
    account_id: 18446744073709551617,
    rack_mask: 0xFFFFFFFFFFFFFFFFFFFF,
    offset: -0x10,
  },
}
"""

FILES["grammar/strings.json5"] = """\
{
  single: 'it\\'s "quoted"',
  double: "say \\"hi\\" and 'bye'",
  escapes: '\\b\\f\\n\\r\\t\\v\\0\\\\\\/',
  other: '\\a\\c\\d\\z\\%',
  hex: '\\x41\\x6c\\x70\\x68\\x61 \\xe9',
  unicode: '\\u00e9t\\u00E9 \\u2603',
  pair: "\\ud83d\\ude00",
  lone: "\\udc00 then \\ud800",
  raw: 'caf\u00e9 \u2603 \U0001f600 \u0627\u0644',
  separators: 'a\u2028b\u2029c',
  continued: 'one \\
two \\\r\nthree \\\u2028four',
  controls: 'tab\there',
  zwj: '\u200d\u200c\u00ad\ufeff',
}
"""

FILES["grammar/keys.json5"] = """\
{
  plain: 1,
  $dollar: 2,
  _under: 3,
  a$b_c9: 4,
  caf\u00e9: 5,
  \u540d\u524d: 6,
  \u01c8ex: 7,
  \u2160\u2161: 8,
  a\u0308o: 9,
  a\u0660: 10,
  a\u203fb: 11,
  \\u0061bc: 12,
  x\\u0041: 13,
  \\u0031x: 14,
  zw\u200cj\u200d: 15,
  while: 16,
  null: 17,
  true: 18,
  Infinity: 19,
  'quoted key': 20,
  "": 21,
  '1abc': 22,
  'new': 23,
  'newbie': 24,
}
"""

FILES["grammar/numbers.json5"] = """\
[
  0, -0, +0, 7, -7, +7,
  123456789012345678901234567890,
  -98765432109876543210,
  0x0, 0xff, 0XFF, -0xff, +0xff, 0xDEADbeef, 0x10000000000000000,
  1.5, -1.5, +1.5, .5, -.5, 5., -5., 0.0, -0.0,
  1e3, 1E3, 1e+3, 1e-3, 2.5e10, -2.5E-10, .5e1, 5.e1,
  1e308, 1e309, -1e309, 5e-324, 2e-324, 1.7976931348623157e308,
  0.1, 0.30000000000000004, 1e16, 1e-5, 123456789.123456789,
  Infinity, +Infinity, -Infinity, NaN, -NaN, +NaN,
]
"""

FILES["grammar/whitespace.json5"] = (
    "\ufeff\u2003// a BOM, an em space and a comment\n"
    "{\u3000a\u00a0:\u2028 1 ,\u000b\u000cb /* inline */ : [ 2 ,\u202f3, ] ,\r\n"
    "  c\t: 'x'// end of line\r"
    "}\u2029\n"
)

FILES["grammar/nonstrict.json5"] = (
    "{\n"
    "  sql: 'SELECT id\n  FROM users\r\n  WHERE active',\n"
    '  bell: "ding\x07 \x1b[0m",\n'
    "}\n"
)

FILES["grammar/dupes.json5"] = """\
{
  host: 'a.example.com',
  port: 8080,
  "host": 'b.example.com',
  nested: {x: 1, y: 2, x: 3},
}
"""

FILES["grammar/stream.json5"] = """\
{event: 'deploy', id: 1}
{event: 'rollback', id: 2} // after the canary failed
[1, 2, 3]
'done'
   \u3000
"""

FILES["grammar/stream_comment.json5"] = "1 2 3 // end\n"

FILES["grammar/stream_bad.json5"] = "{a: 1} {b: 2,, } {c: 3}\n"

# json5's own sample.json5
FILES["sample.json5"] = """\
{
    foo: 'bar',
    while: true,

    this: 'is a \\
multi-line string',

    // this is an inline comment
    here: 'is another', // inline comment

    /* this is a block comment
       that continues on another line */

    hex: 0xDEADbeef,
    half: .5,
    delta: +10,
    to: Infinity,   // and beyond!

    finally: 'a trailing comma',
    oh: [
        "we shouldn't forget",
        'arrays can have',
        'trailing commas too',
    ],
}
"""

BROKEN = {
    "unterminated.json5": "{\n  name: 'web\n}\n",
    "missing_colon.json5": "{\n  name 'web',\n}\n",
    "hyphen_key.json5": "{\n  max-age: 3600,\n}\n",
    "leading_zero.json5": "{port: 0080}\n",
    "bad_exponent.json5": "{timeout: 1e}\n",
    "bad_exponent_sign.json5": "[1.5E+]\n",
    "lone_dot.json5": "[1, ., 3]\n",
    "dot_exponent.json5": "{ratio: .e5}\n",
    "hex_float.json5": "[0x1.8]\n",
    "lone_plus.json5": "[+]\n",
    "units.json5": "{width: 12px}\n",
    "trailing.json5": "{a: 1}}\n",
    "two_values.json5": "{a: 1}\n{b: 2}\n",
    "empty_comma.json5": "{,}\n",
    "double_comma.json5": "[1,,2]\n",
    "comma_only.json5": "[ ,]\n",
    "short_hex.json5": "'\\x4'\n",
    "short_unicode.json5": '"\\u12g4"\n',
    "digit_escape.json5": "'\\1'\n",
    "zero_digit.json5": "'\\01'\n",
    "lowercase_nan.json5": "[nan]\n",
    "undefined.json5": "{x: undefined}\n",
    "nul.json5": "[nul]\n",
    "open_comment.json5": "{a: 1} /* never closed\n",
    "single_slash.json5": "{a: 1} / comment\n",
    "number_key.json5": "{1: 'one'}\n",
    "control_key.json5": "{a\u0007: 1}\n",
    "bare_word.json5": "hello\n",
    "only_comment.json5": "// nothing here\n",
    "whitespace.json5": "  \n\t\n",
    "empty.json5": "",
    "raw_newline.json5": '{key: "value\nover two lines"}\n',
    "raw_cr.json5": '["a\rb"]\n',
    "unclosed_array.json5": "[1, 2,\n",
    "deep_error.json5": "{\n  a: {\n    b: [1, 2, {c: tru}],\n  },\n}\n",
}

BINARY = {
    "broken/latin1.json5": b"{city: 'M\xfcnchen'}\n",
    "broken/latin1_start.json5": b"{\xe9: 1}\n",
}

CASES = [
    ("", "[]"), ("", "[0,1]"), ("", "[ 0 , 1 ]"), ("", "true"), ("", "false"),
    ("", "null"), ("", "{foo: 1, foo: 2}"), ("dups=0", "{foo: 1, foo: 2}"),
    ("dups=0", "{foo: 1, bar: 2}"), ("", "'"), ("", "1"), ("", "-1"),
    ("", "+1"), ("", "--6"), ("", "++6"), ("", "+-6"), ("", "0xf"),
    ("", "0XABCD"), ("", "0x+"), ("", "+0xf"), ("", "-0x0"), ("", "1.5e3"),
    ("", "-0.5e-2"), ("", "--6.0"), ("", "Infinity"), ("", "-NaN"),
    ("", "14d"), ("", "{$: 1}"), ("", "{a$: 1}"), ("", "{1: 1}"),
    ("", "{}"), ("", '{"foo":0,"bar":1}'), ("", "'\\x66oo'"),
    ("", '"\\u0066oo"'), ("", "'\\x0'"), ("", "'\\xj'"), ("", "'\\u000j'"),
    ("", "'\\uj000'"), ("", r'"\/"'), ("", r'"\0"'), ("", "0 1"),
    ("", "0 a"), ("", "4 x"), ("trailing=0", "4 x"),
    ("trailing=0", "[1] [2]"), ("", "\u2000 1"), ("", "1 //"),
    ("", "1 /*"), ("", "{a:1,}"), ("", "[1,]"), ("", "{a:1,,}"),
    ("", "[1 2]"), ("", "{a 1}"), ("", "{'a' 1}"), ("", "{a:}"),
    ("", "Infinityx"), ("", "NaN1"), ("", "1Infinity"), ("", "0x"),
    ("", "0xg"), ("", "00"), ("", "01.5"), ("", "-"), ("", "-x"),
    ("", "-Inf"), ("", "tru"), ("", "nulls"), ("", "'abc"), ("", '"abc'),
    ("", "\"a'b\""), ("", "{\\u0061: 1}"), ("", "{\\u0031: 1}"),
    ("", "{a\\u0020b: 1}"), ("", "{\\x41: 1}"), ("", "[1e]"),
    ("", "1e+"), ("", "."), ("", "-."), ("", "5.e3"),
    ("", "/* c */ 1"), ("", "{/**/a/**/:/**/1/**/}"),
    ("dups=0", "{a: {b: 1, b: 2}, a: 3}"), ("dups=0", "{a: 1e, a: 2}"),
    ("dups=0", "{\"a\": 1, a: 2}"),
]

# Encoder runs over the files above, and the tool.
JOBS = []
for rel in ["config/renovate.json5", "config/package.json5",
            "config/runtime_enabled_features.json5",
            "config/babel.config.json5", "config/inventory.json5",
            "grammar/strings.json5", "grammar/keys.json5",
            "grammar/numbers.json5", "grammar/whitespace.json5",
            "grammar/dupes.json5", "sample.json5"]:
    JOBS.append(["load", rel])
JOBS += [
    ["load", "grammar/dupes.json5", "dups=0"],
    ["load", "grammar/nonstrict.json5"],
    ["load", "grammar/nonstrict.json5", "strict=0"],
    ["load", "grammar/stream.json5"],
    ["load", "grammar/stream.json5", "trailing=0"],
]
for rel in sorted(BROKEN):
    JOBS.append(["load", "broken/" + rel])
for rel in sorted(BINARY):
    JOBS.append(["load", rel])
JOBS += [
    ["load", "broken/raw_newline.json5", "strict=0"],
    ["load", "broken/two_values.json5", "trailing=0"],
    ["load", "broken/trailing.json5", "trailing=0"],
    ["parse", "grammar/stream.json5"],
    ["parse", "grammar/stream_comment.json5"],
    ["parse", "grammar/stream_bad.json5"],
    ["parse", "broken/two_values.json5"],
    ["cases"],
    ["dump", "config/renovate.json5"],
    ["dump", "config/renovate.json5", "indent=2"],
    ["dump", "config/package.json5", "indent=2", "quote_keys=1", "trailing_commas=0"],
    ["dump", "config/package.json5", "indent=4", "sort_keys=1", "quote_style=always_single"],
    ["dump", "config/runtime_enabled_features.json5", "indent=tab"],
    ["dump", "config/runtime_enabled_features.json5", "compact=1"],
    ["dump", "config/babel.config.json5", "indent=0"],
    ["dump", "config/babel.config.json5", "indent=-3", "trailing_commas=0"],
    ["dump", "config/inventory.json5", "indent=2"],
    ["dump", "config/inventory.json5", "allow_nan=0"],
    ["dump", "grammar/strings.json5", "indent=2"],
    ["dump", "grammar/strings.json5", "indent=2", "ensure_ascii=0"],
    ["dump", "grammar/strings.json5", "indent=2", "quote_style=always_single"],
    ["dump", "grammar/strings.json5", "indent=2", "quote_style=prefer_double", "ensure_ascii=0"],
    ["dump", "grammar/strings.json5", "indent=2", "quote_style=prefer_single", "ensure_ascii=0"],
    ["dump", "grammar/keys.json5", "indent=2"],
    ["dump", "grammar/keys.json5", "indent=2", "ensure_ascii=0", "sort_keys=1"],
    ["dump", "grammar/keys.json5", "quote_keys=1"],
    ["dump", "grammar/numbers.json5"],
    ["dump", "grammar/numbers.json5", "allow_nan=0"],
    ["dump", "grammar/whitespace.json5", "indent=s:--"],
    ["dump", "sample.json5", "indent=2", "quote_style=prefer_single"],
    ["dump", "sample.json5", "indent=s:"],
    ["roundtrip", "config/renovate.json5"],
    ["roundtrip", "config/inventory.json5"],
    ["roundtrip", "grammar/strings.json5"],
    ["roundtrip", "grammar/keys.json5"],
    ["roundtrip", "grammar/numbers.json5"],
    ["roundtrip", "sample.json5"],
    ["tool", "data/sample.json5"],
    ["tool", "--as-json", "data/config/renovate.json5"],
    ["tool", "--indent", "2", "--quote-style", "always_single", "data/config/package.json5"],
    ["tool", "--indent", "None", "data/config/babel.config.json5"],
    ["tool", "--indent", "..", "--no-trailing-commas", "data/config/babel.config.json5"],
    ["tool", "--indent", "+1", "--quote-keys", "data/grammar/keys.json5"],
    ["tool", "--no-strict", "data/grammar/nonstrict.json5"],
    ["tool", "data/grammar/nonstrict.json5"],
    ["tool", "--quote-style", "prefer_single", "data/grammar/strings.json5"],
    ["tool", "-c", "{a: [1, 'two', {three: 3.0}], 'b c': null}"],
    ["tool", "-c", "[]"],
    ["tool", "-V"],
    ["tool", "--quote-style", "smart", "-c", "1"],
    ["tool", "data/broken/units.json5"],
    ["tool", "data/broken/empty.json5"],
    ["tool", "data/missing.json5"],
]


def write(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def main():
    files = dict(FILES)
    for rel, text in BROKEN.items():
        files["broken/" + rel] = text
    for rel, text in files.items():
        write(rel, text.encode("utf-8"))
    for rel, b in BINARY.items():
        write(rel, b)
    write("cases.tsv", "".join(o + "\t" + c + "\n" for o, c in CASES).encode("utf-8"))
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in JOBS).encode("utf-8"))


if __name__ == "__main__":
    main()
