#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_requirements: one job per line.

Two ops over the PEP 508 requirement grammar that every `requirements.txt`
line and every package's `Requires-Dist` metadata is written in:

  req  \t <requirement-string>
  eval \t <requirement-string> \t <extra>

`req` parses the requirement and prints its parts (name, sorted extras,
canonical specifier, url). `eval` parses it and evaluates its environment
marker against a fixed environment (a Linux / CPython 3.11.5 profile), with
`<extra>` naming the extra being installed (`-` for none). Both report
`INVALID` for a requirement the grammar rejects.
"""
import os

REQ = [
    "requests",
    "requests>=2.0",
    "requests>=2.0,<3.0",
    "requests[security]",
    "requests[security,socks]",
    "requests[socks,security]",       # extras come out sorted
    "Django>=3.2,<4.0",               # name spelling preserved
    "foo==1.0.0",
    "foo===1.0+local",
    "foo ~= 2.2",                     # spaces around the operator
    "foo != 1.5",
    "pip @ https://example.com/pip.tar.gz",
    "name @ https://example.com/pkg.whl ; python_version < '3.9'",
    "foo ; os_name == 'posix'",       # marker, no specifier
    "foo[a,b]>=1,<2 ; extra == 'a'",  # everything at once
    # rejects
    "",
    "_leading",
    "foo bar",
    "foo>=",
    "foo[]",
]

# eval: (requirement, extra)
EVAL = [
    ("foo; python_version >= '3.8'", "-"),
    ("foo; python_version < '3.8'", "-"),
    ("foo; python_version == '3.11'", "-"),
    ("foo; python_version != '3.10'", "-"),
    ("foo; python_version ~= '3.11'", "-"),
    ("foo; python_full_version >= '3.11.0'", "-"),
    ("foo; '3.8' <= python_version", "-"),      # variable on the right
    ("foo; python_version >= '3.8' and sys_platform == 'linux'", "-"),
    ("foo; python_version < '3.8' or sys_platform == 'linux'", "-"),
    ("foo; sys_platform == 'win32'", "-"),
    ("foo; os_name == 'posix'", "-"),
    ("foo; implementation_name == 'cpython'", "-"),
    ("foo; platform_machine == 'x86_64'", "-"),
    ("foo; 'linux' in sys_platform", "-"),       # substring membership
    ("foo; 'win' not in sys_platform", "-"),
    ("foo; sys_platform > 'a'", "-"),            # '>' on a string marker is always false
    ("foo; (python_version >= '3.8' and sys_platform == 'linux') or os_name == 'nt'", "-"),
    ("foo", "-"),                                # no marker
    ("foo; extra == 'dev'", "dev"),
    ("foo; extra == 'dev'", "-"),
    ("foo; extra == 'dev'", "test"),
    ("foo; extra == 'Dev'", "dev"),              # extra names normalize (PEP 503)
    ("foo; extra == 'dev' and python_version >= '3.8'", "dev"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for r in REQ:
        fh.write("req\t" + r + "\n")
    for r, extra in EVAL:
        fh.write("eval\t" + r + "\t" + extra + "\n")
