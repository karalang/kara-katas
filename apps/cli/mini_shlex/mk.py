#!/usr/bin/env python3
"""Writes data/: a project tree for the glob jobs, and data/jobs.tsv.

A job is one line of tab-separated fields. In a field, a "⏎" stands for a
newline and a "⇥" for a tab.
"""
import os

os.makedirs("data/tree", exist_ok=True)
FILES = [
    "Procfile", "Makefile", "README.md", "setup.cfg", ".env", ".gitignore",
    "src/app.py", "src/util.py", "src/__init__.py", "src/.cache.py",
    "src/models/user.py", "src/models/order.py", "src/models/__init__.py",
    "src/models/.hidden/secret.py", "tests/test_app.py", "tests/test_util.py",
    "tests/data/sample[1].json", "tests/data/sample2.json", "tests/data/notes.txt",
    "docs/index.md", "docs/api/v1.md", "docs/api/v2.md", "docs/api/v10.md",
    ".github/workflows/ci.yml", "build/lib/app.py", "a*b/star.txt", "q?/mark.txt",
    "Ünïcode/café.txt", "empty/", "data.tar.gz", "data.tgz", "photo.JPG", "photo.jpg",
]
for f in FILES:
    p = os.path.join("data/tree", f)
    if f.endswith("/"):
        os.makedirs(p, exist_ok=True)
        continue
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        fh.write(f + "\n")

JOBS = r"""
split	1	0	ls -la /tmp
split	1	0	echo "hello world" 'single quoted' plain
split	1	0	a\ b c\\d "e\"f" 'g\'h
split	1	0	a\ b c\\d "e\"f" 'g\h'
split	1	0	"a"'b'c d""e ''
split	1	0	cmd --opt="value with spaces" --flag
split	1	0	echo $HOME "${PATH}" '$USER'
split	1	0	foo#bar # trailing comment
split	1	1	foo#bar # trailing comment
split	1	1	# only a comment
split	1	1	one⏎two # c⏎three
split	1	0	"unterminated
split	1	0	'unterminated
split	1	0	trailing\
split	1	0	
split	1	0	   ⇥   
split	1	0	"\$ \` \" \\ \n"
split	1	0	'\$ \` \" \\ \n'
split	1	0	café "naïve façade" Ünïcode
split	0	0	"a b" 'c d' e\ f
split	0	0	a"b c"d
split	0	1	x # y
split	0	0	"unterminated
split	1	0	git commit -m "fix: handle \"quoted\" args" --author='A <a@b.c>'
split	1	0	ssh host 'cd /srv && ./run.sh --port=8080'
split	1	0	find . -name '*.py' -exec grep -l "TODO" {} \;
lex	posix	ls -la /tmp ; echo hi
lex		ls -la /tmp ; echo hi
lex	posix,ws	a=1 b=2;c=3 d|e
lex	posix,punct	a=1 b=2;c=3 d|e&&f||g
lex	posix,punct	cat < in.txt > out.txt 2>&1 &
lex	posix,punct	(cd sub && make) | tee log
lex	punct	a;b "c;d" 'e;f'
lex	posix,punct=;	a;b|c
lex	posix,punct,ws	a=1 b=2;c=3 ~/x.y
lex	posix,nocomment	a # b
lex		a.b-c/d e+f
lex	posix	a.b-c/d e+f
lex	punct	a.b-c/d e+f ~x
lex		x'y z'w "q r"
lex	posix	one⏎# comment⏎two three⏎four
lex	posix,ws	one⏎# comment⏎two three⏎four
quote	simple
quote	
quote	has space
quote	it's
quote	$HOME
quote	a"b
quote	-flag=1
quote	path/to/file.txt
quote	@%+=:,./-
quote	tab⇥here
quote	café
quote	semi;colon
join	ls	-la	my file
join	echo	it's	"q"	
join	
fnmatch	app.py	*.py
fnmatch	app.py	*.PY
fnmatch	app.py	a??.py
fnmatch	app.py	[ab]pp.py
fnmatch	app.py	[!a]pp.py
fnmatch	src/app.py	*.py
fnmatch	src/app.py	src/*
fnmatch	.env	*
fnmatch	.env	.*
fnmatch	v10.md	v[0-9].md
fnmatch	v1.md	v[0-9].md
fnmatch	v1.md	v[!0-9].md
fnmatch	a]b	a[]]b
fnmatch	a-b	a[a-]b
fnmatch	a-b	a[-a]b
fnmatch	a-b	a[!-]b
fnmatch	a[b	a[b
fnmatch	a[b	a[[]b
fnmatch	ab	a[z-a]b
fnmatch	a-b	a[z-a-]b
fnmatch	ab	a[!]b
fnmatch	a!b	a[!]b
fnmatch	a\b	a\b
fnmatch	a\b	a[\]b
fnmatch	abc	*a*b*c*
fnmatch	abcabd	*ab?
fnmatch	café.txt	caf?.txt
fnmatch	café.txt	*[é].txt
fnmatch	a^b	a[^]b
fnmatch	a^b	a[\^]b
fnmatch	x	[a-c-z]
fnmatch	-	[a-c-z]
fnmatch	b	[a-c-z]
fnmatch	*	[*]
fnmatch	line⏎break	line?break
fnmatch	line⏎break	line*
filter	*.py	app.py	util.py	README.md	.cache.py	setup.cfg
filter	*.[ch]	a.c	b.h	c.cc	d.hh	.e.c
filter	[!.]*	.env	env	..	x
glob	*	0	0
glob	*	0	1
glob	.*	0	0
glob	*.md	0	0
glob	src/*.py	0	0
glob	src/*	0	0
glob	src/*	0	1
glob	*/*.py	0	0
glob	**	0	0
glob	**	1	0
glob	**	1	1
glob	**/*.py	1	0
glob	**/*.py	1	1
glob	src/**	1	0
glob	src/**/	1	0
glob	**/	1	0
glob	src/**/*.py	1	0
glob	docs/**/v?.md	1	0
glob	docs/**/v*.md	0	0
glob	*/	0	0
glob	*/	0	1
glob	tests/data/sample[1].json	0	0
glob	tests/data/sample[[]1].json	0	0
glob	tests/data/sample[12].json	0	0
glob	a*b/*	0	0
glob	a[*]b/*	0	0
glob	q[?]/*	0	0
glob	Ü*/*	0	0
glob	photo.*	0	0
glob	*.t*gz	0	0
glob	*.tar.gz	0	0
glob	README.md	0	0
glob	missing.txt	0	0
glob	src/	0	0
glob	missing/	0	0
glob	empty/*	0	0
glob	empty/**	1	0
glob	*/*/*/*.py	0	0
glob	src/models/.hidden/*	0	0
glob	src/*/.hidden/*	0	0
glob	src/**/secret.py	1	0
glob	src/**/secret.py	1	1
glob	[!.]*file	0	0
escape	tests/data/sample[1].json
escape	a*b/star.txt
escape	q?/mark.txt
escape	plain/path.txt
escape	[[]]
"""
with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))
