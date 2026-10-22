#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_identify: one job per line, `op \t arg`.

The jobs exercise the way pre-commit identifies a file from its name and shebang
alone (no filesystem): tags_from_filename over plain extensions, uppercase
extensions, double extensions (only the last counts), leading-dot names with no
extension, the NAMES table (and the "Dockerfile.xenial matches Dockerfile"
dot-split fallback), the EXTENSIONS_NEED_BINARY_CHECK table, and misses;
tags_from_interpreter with the python3.5.2 -> python3.5 -> python3 narrowing and
a /usr/bin path prefix; and parse_shebang with the /usr/bin/env and
`/usr/bin/env -S` rewrites, a direct interpreter path, and non-shebangs.
"""
import os

JOBS = [
    ("filename", "foo.py"),
    ("filename", "README.md"),
    ("filename", "script.PY"),           # uppercase ext -> lowered
    ("filename", "archive.tar.gz"),      # only the last ext (gz) counts
    ("filename", "bundle.min.js"),
    ("filename", ".bashrc"),             # leading-dot NAME, no ext
    ("filename", ".babelrc"),
    ("filename", "Dockerfile"),          # NAMES
    ("filename", "Dockerfile.xenial"),   # NAMES via dot-split fallback
    ("filename", "Makefile"),
    ("filename", "setup.cfg"),
    ("filename", "image.ppm"),           # EXTENSIONS_NEED_BINARY_CHECK
    ("filename", "config.plist"),        # EXTENSIONS_NEED_BINARY_CHECK
    ("filename", "src/main/app.rs"),     # basename only
    ("filename", "mystery.zzz"),         # miss
    ("filename", "noextension"),         # miss
    ("interpreter", "python"),
    ("interpreter", "python3.5.2"),      # narrows to python3
    ("interpreter", "/usr/bin/python3.6"),
    ("interpreter", "bash"),
    ("interpreter", "ruby"),
    ("interpreter", "node"),
    ("interpreter", "weirdlang9"),       # miss
    ("shebang", "#!/usr/bin/env python3"),
    ("shebang", "#!/usr/bin/python"),
    ("shebang", "#!/usr/bin/env -S python -u"),
    ("shebang", "#!/bin/sh"),
    ("shebang", "#!/usr/bin/env"),       # env with nothing after -> empty
    ("shebang", "not a shebang"),        # no #! -> empty
    ("shebang_tags", "#!/usr/bin/env python3.11"),
    ("shebang_tags", "#!/bin/bash"),
    ("shebang_tags", "#!/usr/bin/perl"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
