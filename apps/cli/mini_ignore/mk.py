# Writes the inputs of mini_ignore into data/: a monorepo's working tree
# with .gitignore files at several levels, and the repository's
# .git/info/exclude as data/exclude.txt.
import os, shutil

shutil.rmtree("data", ignore_errors=True)

def put(path, text="x\n"):
    full = "data/repo/" + path
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", newline="") as f:
        f.write(text)

put(".gitignore", """# OS and editor files
.DS_Store
*.swp
*~
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json

# build output
/build/
dist/
target/
*.[oa]
!keep.o
*.py[cod]
__pycache__/
node_modules/
cache/

# logs, but keep the important one and the logs directory itself
*.log
!important.log
logs/**
!logs/.gitkeep

# secrets
.env
.env.*
!.env.example

# patterns
doc/**/*.pdf
**/tmp
a/**/b
abc/**
**/deep/x
foo/*/bar
[Dd]ebug/
/*.tmp
data-[0-9][0-9].csv
report[!x].txt
[[:upper:]]*.bak
mid**dle.txt
\\#notes.txt
\\!bang
star\\*.txt
trailing-space\\ 
trailing-spaces   
space\\ inside.txt
""")
for p in ["README.md", "Makefile", "main.c", "util.h", "main.o", "lib.a", "keep.o", ".DS_Store",
          "notes.txt~", "main.c.swp", ".idea/workspace.xml", ".idea/modules/app.iml",
          ".vscode/settings.json", ".vscode/launch.json", ".vscode/extensions.json",
          "build/out.bin", "build/sub/x.txt", "dist/app.js", "important.log", "debug.log",
          "logs/.gitkeep", "logs/today.log", "logs/README", "logs/old/2026-09.log",
          ".env", ".env.local", ".env.example", "doc/manual.pdf", "doc/guide.md",
          "doc/api/v1/ref.pdf", "doc/api/v1/ref.md", "a/b", "a/c", "a/x/y/b", "a/x/b/inner.txt",
          "abc/x/y.txt", "abc.txt", "deep/x", "src/deep/x", "src/deep/y", "foo/one/bar", "foo/one/two/bar",
          "foo/bar", "x.tmp", "src/y.tmp", "data-01.csv", "data-1.csv", "data-001.csv",
          "report1.txt", "reportx.txt", "report10.txt", "Old.bak", "old.bak", "middle.txt",
          "mid-and-middle.txt", "midd/le.txt", "#notes.txt", "!bang", "star*.txt", "starX.txt",
          "trailing-space ", "trailing-space", "trailing-spaces", "space inside.txt",
          "node_modules/left-pad/index.js", "cache", "lib/cache/blob", "lib/cache.txt",
          "local-notes/todo.txt", "key.secret", "keys/prod.secret",
          "src/app.py", "src/app.pyc", "src/util.pyc", "src/__pycache__/app.cpython-313.pyc",
          "src/build/gen.c", "src/x.gen.c", "src/local.cfg", "src/nested/local.cfg",
          "src/debug/trace.txt", "src/Debug/trace.txt", "src/tmp/scratch.txt", "src/tmpfile",
          "packages/web/package.json", "packages/web/dist/keep.txt", "packages/web/dist/bundle.js",
          "packages/web/node_modules/react/index.js", "packages/web/settings.local",
          "packages/web/src/index.ts", "packages/api/server.log", "packages/api/main.rs",
          "packages/api/target/release/api", "packages/legacy/old.bak", "packages/legacy/new.txt",
          "packages/legacy/stuff.orig", "packages/legacy/sub/also.orig"]:
    put(p)
put("src/.gitignore", "# python bytecode is ignored at the top, but this one is checked in\n!app.pyc\n*.gen.c\n/local.cfg\n")
put("packages/web/.gitignore", "dist\n!dist/keep.txt\n*.local\n")
put("packages/api/.gitignore", "!*.log\n")
put("packages/legacy/.gitignore", "# written on Windows\r\n*.bak\r\n*.orig\r\n!sub/also.orig")
os.makedirs("data", exist_ok=True)
with open("data/exclude.txt", "w") as f:
    f.write("# git ls-files --others --exclude-from=.git/info/exclude\n# Lines that start with '#' are comments.\nlocal-notes/\n*.secret\n")
