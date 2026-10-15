# Writes data/: path strings, path operations, a source tree and the
# rules that select from it.
import os, shutil
shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")

paths = [
    ("posix", ""), ("posix", "."), ("posix", "a/b.tar.gz"), ("posix", "/etc/hosts"),
    ("posix", "//net/share/x"), ("posix", "///usr//lib/./x.so.1"), ("posix", "a/../b"),
    ("posix", ".bashrc"), ("posix", "archive."), ("posix", "x/.config.d/"), ("posix", "/"),
    ("posix", "..."), ("posix", "a\\b.txt"), ("posix", "src/main.c"), ("posix", "c:/win"),
    ("posix", "./a/./b/"), ("posix", "name with space.tar.bz2"), ("posix", ".tar.gz"),
    ("win", ""), ("win", "c:\\Windows\\System32\\drivers\\etc\\hosts"), ("win", "C:/Program Files/App/app.exe"),
    ("win", "c:relative\\x.txt"), ("win", "\\rooted\\only"), ("win", "\\\\server\\share\\dir\\f.doc"),
    ("win", "//server/share"), ("win", "\\\\server"), ("win", "\\\\?\\c:\\very\\long"),
    ("win", "\\\\?\\UNC\\srv\\sh\\x"), ("win", "\\\\.\\PhysicalDrive0"), ("win", "a/b\\c.d.e"),
    ("win", "d:"), ("win", "d:\\"), ("win", "x:y:z"), ("win", "./c:x"), ("win", "nul.txt"),
    ("win", "a\\..\\b"), ("win", "\\\\?\\Volume{1}\\f"),
]
with open("data/paths.txt", "w") as f:
    for fl, p in paths:
        f.write(f"{fl}\t{p}\n")

ops = [
    "join posix a b c", "join posix a /b c", "join posix /a/ b//c ./d", "join posix  a",
    "join posix a ", "join win c:\\a d:b", "join win c:\\a \\b", "join win c:\\a C:b",
    "join win c:\\a c:b", "join win \\\\srv\\sh x", "join win //srv/sh \\\\srv\\sh\\y",
    "join win a c:", "join win c: x", "join win \\\\srv\\sh\\ \\x",
    "with_name posix a/b.txt c.py", "with_name posix a/b.txt ", "with_name posix a/b.txt x/y",
    "with_name posix a/b.txt .", "with_name posix / x", "with_name posix a/b.txt ..",
    "with_name win c:\\a\\b x/y", "with_name win c:\\ x", "with_name win a\\b c:d",
    "with_name posix a/b x\\y",
    "with_suffix posix a/b.txt .md", "with_suffix posix a/b.tar.gz .zip", "with_suffix posix a/b.txt ",
    "with_suffix posix a/b md", "with_suffix posix a/b .", "with_suffix posix a/.bashrc .bak",
    "with_suffix posix / .x", "with_suffix posix a/b. .c", "with_suffix posix a/b .a.b",
    "with_suffix win c:\\x\\y.TXT .doc", "with_suffix posix a/b ./c",
    "with_stem posix a/b.txt c", "with_stem posix a/b.txt ", "with_stem posix a/b c",
    "with_stem posix a/b ", "with_stem posix a/.x y", "with_stem posix a/b.tar.gz c",
    "relative_to posix /etc/passwd /", "relative_to posix /etc/passwd /etc",
    "relative_to posix /etc/passwd /usr", "relative_to posix /etc/passwd /usr walk",
    "relative_to posix a/b/c a", "relative_to posix a/b/c a/b/c", "relative_to posix a /a",
    "relative_to posix a /a walk", "relative_to posix a/b x/../y walk",
    "relative_to posix a/b x/y/z walk", "relative_to posix /a/b //a walk",
    "relative_to win C:\\Users\\Bob\\f c:\\users", "relative_to win C:\\Users\\Bob\\f d:\\ walk",
    "relative_to win C:\\a\\b c:\\x\\y walk", "relative_to win \\\\s\\h\\a \\\\S\\H",
    "relative_to posix a/b ", "relative_to posix a/b a/b/c walk",
    "is_relative_to posix /a/b /a", "is_relative_to posix /a/b /A",
    "is_relative_to win c:\\a\\b C:/A", "is_relative_to posix a/b b",
    "match posix a/b.py *.py", "match posix /a/b/c.py b/*.py", "match posix /a/b/c.py /*.py",
    "match posix /a/b/c.py /a/*/*.py", "match posix a/b.py ", "match posix a/b.PY *.py",
    "match win C:\\a\\B.PY *.py", "match win c:\\a\\b.py C:/a/*", "match posix a/b/c **",
    "match posix a/b.py a/b.py/c", "match posix x/y [xz]/[!a-c]",
    "full_match posix a/b/c.py **/*.py", "full_match posix c.py **/*.py",
    "full_match posix a/b/c.py *.py", "full_match posix a/b/c.py a/**",
    "full_match posix a a/**", "full_match posix a/b/c a/**/c", "full_match posix a/c a/**/c",
    "full_match posix a/.hidden/x */*/x", "full_match posix . *", "full_match posix  **",
    "full_match posix /a/b /**", "full_match posix a/b/c **/**/c", "full_match win C:\\X\\y.TXT c:/x/*.txt",
    "full_match posix f1.txt f[0-9].txt", "full_match posix fa.txt f[!0-9].txt",
    "full_match posix a/b a?b", "full_match posix a[/]b a[/]b", "full_match posix x.c *.[ch]",
    "full_match posix ab a**b", "full_match posix a/xb/c a/*b/c",
    "eq posix a/b a//b/", "eq posix a/b A/B", "eq win a\\b A/B", "eq win c:\\a C:\\A\\",
    "lt posix a/b a-b", "lt posix a-b a/b", "lt win A\\b a\\B", "lt posix /a a",
    "uri posix /etc/hosts", "uri posix /a b/c%d#e", "uri posix a/b", "uri win c:\\Program Files\\x",
    "uri win \\\\srv\\share\\f.txt", "uri win \\rooted", "uri posix //host/x", "uri win c:x",
    "sort posix b a/b a-b a /a A ./c",
    "sort win B a\\b A-b c: \\\\s\\h a c:\\",
]
with open("data/ops.txt", "w") as f:
    for o in ops:
        a = o.split(" ", 2) if o.startswith("uri") else o.split(" ")
        f.write("\t".join(a) + "\n")

tree = [
    "pyproject.toml", "README.md", ".gitignore", ".env",
    "src/pkg/__init__.py", "src/pkg/core.py", "src/pkg/util/strings.py", "src/pkg/util/__init__.py",
    "src/pkg/util/cache.cpython-313.pyc", "src/pkg/data/schema.json", "src/pkg/data/logo.PNG",
    "src/pkg/_native/fast.c", "src/pkg/_native/fast.h", "src/pkg/_native/fast.o",
    "src/pkg-extras/plugin.py", "src/pkg.egg-info/PKG-INFO",
    "tests/test_core.py", "tests/conftest.py", "tests/data/case 1.txt", "tests/data/case2.tar.gz",
    "docs/index.md", "docs/api/core.md", "docs/_build/html/index.html",
    "build/lib/pkg/core.py", "dist/pkg-1.0.tar.gz", "dist/pkg-1.0-py3-none-any.whl",
    ".venv/lib/site.py", "scripts/release.sh", "a/b.txt", "a-b/c.txt",
]
for p in tree:
    os.makedirs(os.path.dirname("data/tree/" + p) or "data/tree", exist_ok=True)
    with open("data/tree/" + p, "w") as f:
        f.write(f"contents of {p}\n")

with open("data/rules.txt", "w") as f:
    f.write("""# last matching rule wins; files no rule names are left out
include **
exclude .*
exclude **/.*/**
exclude build/**
exclude dist/**
exclude docs/_build/**
exclude **/*.py[co]
exclude **/*.o
exclude src/*.egg-info/**
include .gitignore
include dist/*.whl
""")
