# Writes data/ for mini_editorconfig: a directory tree under data/root
# (which the run treats as /) holding the .editorconfig files of a web
# project, a monorepo, a C project, a vendored library and some broken or
# awkward files, plus the jobs: `editorconfig` command lines and glob
# patterns to translate and match.
import json
import os
import random
import shutil

D = "data"
ROOT = os.path.join(D, "root")


def w(path, text, raw=False):
    p = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(text if raw else text.encode("utf-8"))


if os.path.isdir(D):
    shutil.rmtree(D)
os.makedirs(ROOT)

# ---------------------------------------------------------------- a web app
w("/web/.editorconfig", """\
# EditorConfig is awesome: https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = LF
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 120

[*.{js,jsx,ts,tsx,json,yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
max_line_length = off

[Makefile]
indent_style = Tab

[{package.json,.travis.yml}]
indent_size = 2

[lib/**.js]
indent_style = space ; old code
indent_size = 2

[/docs/*.rst]
indent_size = 3

[*.py]
max_line_length = 88  # black's default

[*.min.{js,css}]
indent_style = unset
insert_final_newline = unset
""")
w("/web/legacy/.editorconfig", """\
; the old jQuery code base keeps its tabs
[*.js]
indent_style = tab
tab_width = 8

[vendor/**]
charset = latin1
""")
w("/web/legacy/vendor/.editorconfig", """\
root=TRUE
[*]
indent_style=space
indent_size=tab
tab_width=3
""")
w("/web/src/components/.editorconfig", """\
[*.tsx]
quote_type = single
spelling_language = en-US
""")

# ---------------------------------------------------------------- a monorepo
w("/mono/.editorconfig", """\
root = true

[*]
end_of_line = lf
insert_final_newline = true

[packages/*/src/**.{ts,tsx}]
indent_style = space
indent_size = 2

[packages/{core,cli}/**]
max_line_length = 100

[**/test/fixtures/**]
trim_trailing_whitespace = false
insert_final_newline = false

[migrations/{1..20}_*.sql]
indent_size = 4

[logs/app-{01..12}.log]
charset = utf-8-bom

[shard{-3..3}.conf]
indent_style = tab

[{*.lock,go.sum}]
generated_code = true

[docs/**/*.md]
indent_size = 2

[*.{,s}css]
indent_size = 2

[{a,b{c,d}}.txt]
nested = yes

[{1..3}/notes.txt]
numbered = dir
""")
w("/mono/packages/cli/.editorconfig", """\
[*]
INDENT_SIZE = 8
Indent_Style = SPACE

[src/commands/*.ts]
indent_size = 4
""")

# ---------------------------------------------------------------- a C project
w("/kernel/.editorconfig", """\
# SPDX-style header comment
root = true

[{*.{awk,c,dts,dtsi,dtso,h,mk,s,S},Kconfig,Makefile,Makefile.*}]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = tab
indent_size = 8

[*.{json,py,rs}]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4

[*.yaml]
indent_style = space
indent_size = 2

[scripts/checkpatch.pl]
indent_style = tab
tab_width = 8

[Documentation/**.rst]
indent_style = space
indent_size = 3
""")

# ---------------------------------------------------------------- awkward files
w("/odd/.editorconfig", ("\ufeffroot = true\r\n"
                         "[*.txt]\r\n"
                         "indent_size = 2\r\n"
                         "\r\n"
                         "[\\#notes.txt]\r\n"
                         "comment_char = \\#\r\n"
                         "[a\\;b.txt]\r\n"
                         "semi = no\r\n"
                         "[*.ini] ; trailing comment\r\n"
                         "value = \"\"\r\n"
                         "note = keep #this; and ;this too\r\n"
                         "spaced = a ;b\r\n"
                         "hashed = x #y\r\n"
                         "colon: works too\r\n"
                         "   leading = whitespace   \r\n"
                         "[*.conf]\r\n"
                         "Unicode = naïve café\r\n"
                         "empty =\r\n"
                         "eq = a=b=c\r\n"
                         "[weird]]name]\r\n"
                         "bracket = yes\r\n"
                         "[[x].dat]\r\n"
                         "brackets = nested\r\n"))
w("/odd/old-mac/.editorconfig", "[*]\rindent_size = 6\rcr_only = true\r")
w("/broken/.editorconfig", """\
root = true
[*]
indent_size = 4
this line has no separator
[*.c]
= no name
indent_style = tab
  just words
[*.h
tab_width = 4
""")
w("/regex/.editorconfig", """\
root = true
[*]
base = yes
[[z-a].txt]
never = reached
""")
w("/regex2/.editorconfig", """\
root = true
[{x,[}]y}.txt]
paren = unbalanced
""")
w("/numgroup/.editorconfig", """\
root = true
[{a,{1..3}}.txt]
picked = yes
""")
w("/alt/.ec", """\
root = true
[*]
alt = file
indent_style = tab
""")
w("/alt/.editorconfig", """\
root = true
[*]
alt = no
""")
w("/version/.editorconfig", """\
root = true
[*.go]
indent_style = tab
[*.mk]
indent_style = tab
indent_size = 4
[*.tsv]
indent_size = tab
""")
w("/latin/.editorconfig", "root = true\n[*.txt]\nname = caf\u00e9\n")
os.makedirs(os.path.join(ROOT, "dironly", ".editorconfig"))
w("/dironly/sub/.editorconfig", "[*]\nfrom = sub\n")

# ---------------------------------------------------------------- jobs
jobs = []


def ec(*args):
    jobs.append(["ec", list(args)])


for f in ["/web/index.html", "/web/src/app.js", "/web/src/App.tsx", "/web/src/components/Button.tsx",
          "/web/package.json", "/web/.travis.yml", "/web/Makefile", "/web/src/Makefile",
          "/web/lib/util.js", "/web/lib/deep/er/util.js", "/web/docs/index.rst", "/web/docs/api/index.rst",
          "/web/README.md", "/web/tools/build.py", "/web/dist/app.min.js", "/web/dist/app.min.css",
          "/web/legacy/jquery.js", "/web/legacy/vendor/plugin.js", "/web/legacy/vendor/deep/x.css",
          "/web/legacy/notes.md", "/web/src/../lib/x.js", "/web//src///app.js", "/web/./README.md"]:
    ec(f)
ec("/web/src/app.js", "/web/README.md", "/web/Makefile")
for f in ["/mono/packages/core/src/index.ts", "/mono/packages/core/src/a/b/c.tsx", "/mono/packages/core/lib/x.ts",
          "/mono/packages/cli/src/commands/init.ts", "/mono/packages/cli/README.md", "/mono/packages/web/src/x.ts",
          "/mono/test/fixtures/a.txt", "/mono/packages/core/test/fixtures/deep/b.json",
          "/mono/migrations/1_init.sql", "/mono/migrations/07_users.sql", "/mono/migrations/20_x.sql",
          "/mono/migrations/21_x.sql", "/mono/migrations/0_zero.sql", "/mono/migrations/+5_plus.sql",
          "/mono/logs/app-01.log", "/mono/logs/app-1.log", "/mono/logs/app-12.log", "/mono/logs/app-13.log",
          "/mono/shard-3.conf", "/mono/shard0.conf", "/mono/shard+2.conf", "/mono/shard4.conf", "/mono/shard-0.conf",
          "/mono/yarn.lock", "/mono/go.sum", "/mono/docs/guide/intro.md", "/mono/docs/intro.md",
          "/mono/style.css", "/mono/style.scss", "/mono/style.sss", "/mono/a.txt", "/mono/bc.txt", "/mono/bd.txt",
          "/mono/b.txt", "/mono/2/notes.txt", "/mono/4/notes.txt", "/mono/x/2/notes.txt"]:
    ec(f)
for f in ["/kernel/kernel/sched/core.c", "/kernel/include/linux/sched.h", "/kernel/Makefile", "/kernel/arch/x86/Makefile.um",
          "/kernel/Kconfig", "/kernel/scripts/checkpatch.pl", "/kernel/tools/perf/util.py", "/kernel/rust/kernel/lib.rs",
          "/kernel/Documentation/process/coding-style.rst", "/kernel/arch/arm64/boot/dts/x.dts", "/kernel/x.S",
          "/kernel/arch/x86/entry/entry_64.s", "/kernel/scripts/gdb/x.awk", "/kernel/Documentation/devicetree/bindings/a.yaml"]:
    ec(f)
for f in ["/odd/readme.txt", "/odd/#notes.txt", "/odd/a;b.txt", "/odd/setup.ini", "/odd/app.conf", "/odd/weird]]name",
          "/odd/[x].dat", "/odd/x.dat", "/odd/old-mac/a.txt"]:
    ec(f)
ec("/broken/main.c")
ec("/broken/x.h", "/web/README.md")
ec("/regex/a.txt")
ec("/regex2/x.txt")
ec("/numgroup/a.txt")
ec("/numgroup/2.txt")
ec("/numgroup/7.txt")
ec("-f", ".ec", "/alt/x.txt")
ec("/alt/x.txt")
ec("-f", "nothing-here", "/alt/x.txt")
for b in ["0.9.0", "0.10.0", "0.17.1", "0.17.1.dev", "0.18.0", "1.0.0", "0.9", "v1.0.0", "0.17.0-beta"]:
    ec("-b", b, "/version/main.go", "/version/rules.mk", "/version/data.tsv")
ec("/version/main.go", "/version/data.tsv")
ec("/latin/x.txt")
ec("/dironly/sub/x.c")
ec("relative/path.c")
ec("/web/src/app.js", "relative.c")
ec()
ec("-v")
ec("--version")
ec("-h")
ec("--help", "/web/x")
ec("-x", "/web/x")
ec("-f")
ec("--verbose")
ec("--version=2")
ec("-b")
ec("-fx", "/alt/x.txt")
ec("-b0.9.0", "/version/main.go")
ec("--", "/web/README.md")
ec("/web/README.md", "-v")
ec("-v", "-h")

PATTERNS = [
    ("*.py", ["a.py", "dir/a.py", ".py", "a.pyc"]),
    ("**.py", ["a.py", "dir/a.py", "x/y/z.py"]),
    ("**/*.py", ["a.py", "/a.py", "dir/a.py"]),
    ("a/**/b", ["a/b", "a/x/b", "a/x/y/b", "ab"]),
    ("?.txt", ["a.txt", "ab.txt", "/.txt"]),
    ("[abc].txt", ["a.txt", "d.txt", "[abc].txt"]),
    ("[!abc].txt", ["a.txt", "d.txt", "!.txt"]),
    ("[^abc].txt", ["d.txt", "^.txt"]),
    ("[a-c]x", ["bx", "-x", "dx"]),
    ("[a/b]c", ["[a/b]c", "a/bc", "ac"]),
    ("[*]", ["*", "x", "]", "*]", "xx]"]),
    ("[?*]", ["?", "a", "ab]", "[ab]"]),
    ("{a,b}.c", ["a.c", "b.c", "ab.c", "{a,b}.c"]),
    ("{a}.c", ["a.c", "{a}.c"]),
    ("{a,b.c", ["{a,b.c", "a"]),
    ("a,b", ["a,b", "a"]),
    ("{a\\,b,c}", ["a,b", "c", "a"]),
    ("\\*.txt", ["*.txt", "a.txt"]),
    ("\\\\x", ["\\x"]),
    ("{1..5}", ["1", "5", "6", "0", "03", "-1", "+3"]),
    ("{-10..-5}", ["-7", "-11", "-5"]),
    ("{5..1}", ["3"]),
    ("{1..3x}", ["2"]),
    ("{a,{1..3}}", ["a", "2"]),
    ("{}.c", ["{}.c", ".c"]),
    ("{,a}.c", [".c", "a.c"]),
    ("{a,b}{1..2}", ["a1", "b2", "c1"]),
    ("a-b", ["a-b"]),
    ("[a-]", ["a", "-", "b"]),
    ("[]a]", ["]", "a"]),
    ("[a\\]b]", ["]", "b", "a"]),
    ("x[", ["x["]),
    ("x]", ["x]"]),
    ("[z-a]", ["a"]),
    ("[{a,b}]", ["a", "(", "|"]),
    ("{[a,b]}", ["[a", "b]"]),
    ("a.{c,cpp,h}", ["a.c", "a.cpp", "a.hpp"]),
    ("**", ["a/b/c", ""]),
    ("*", ["a/b", "ab", ""]),
    ("/a", ["/a", "a"]),
    ("a//b", ["a//b"]),
    ("a/**/", ["a/", "a/b/"]),
    ("$^+()|.&~# ", ["$^+()|.&~# "]),
    ("é?", ["éa", "e"]),
    ("{a,b", ["{a,b"]),
    ("a}", ["a}"]),
    ("{{a,b},c}", ["a", "b", "c", "{a"]),
    ("[a,b]", ["a", ",", "|"]),
    ("[\\-]", ["-", "\\"]),
    ("[\\d]", ["d", "1"]),
]
for p, names in PATTERNS:
    jobs.append(["glob", p, names])

# random section headers over a random file list
rnd = random.Random(1019)
parts = ["src", "lib", "test", "a", "b", "x1", "x2"]
leaves = ["main.c", "util.h", "a.py", "b.py", "x.md", "Makefile", "1.txt", "12.txt", "a.min.js"]
files = sorted({"/".join(rnd.choice(parts) for _ in range(rnd.randint(0, 2))) + "/" + rnd.choice(leaves) for _ in range(60)})
files = [f.lstrip("/") for f in files]
dirs = ["*", "**", "?", "src", "lib", "a", "b", "x[12]", "[!a]*", "{src,lib}", "test", "{a,b}", "x?", "[a-z]*"]
leafs = ["*.c", "*.h", "*.py", "*.{c,h}", "{1..20}.txt", "*.min.*", "Makefile", "[a-z]*", "{a,b}.py", "*",
         "{,x}1*", "x.md", "?.py", "**.md", "[!a-m]*"]
for k in range(40):
    p = "/".join([rnd.choice(dirs) for _ in range(rnd.randint(0, 2))] + [rnd.choice(leafs)])
    if rnd.random() < 0.25:
        p = "/" + p
    jobs.append(["glob", p, files])

with open(os.path.join(D, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("%d jobs" % len(jobs))
