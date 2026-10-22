#!/usr/bin/env python3
"""Writes data/jobs.tsv: one semver operation per line, tab-separated.

op and arg. arg encodings:
  parse     VERSION
  valid     VERSION
  cmp       A|B
  match     VERSION|EXPR
  bump      WHICH|VERSION      WHICH = major/minor/patch/prerelease/build
  next      PART|VERSION       PART  = major/minor/patch/prerelease
  finalize  VERSION
"""
import os

JOBS = [
    # parse: valid and the invalid forms the grammar rejects
    ("parse", "1.2.3"),
    ("parse", "3.4.5-pre.2+build.4"),
    ("parse", "1.0.0-alpha"),
    ("parse", "1.0.0-alpha.1"),
    ("parse", "1.0.0-0.3.7"),
    ("parse", "1.0.0-x.7.z.92"),
    ("parse", "1.0.0+20130313144700"),
    ("parse", "1.0.0-beta+exp.sha.5114f85"),
    ("parse", "01.2.3"),            # leading zero in major
    ("parse", "1.2"),              # missing patch
    ("parse", "1.2.3.4"),          # extra part
    ("parse", "1.2.3-01"),         # leading zero in numeric prerelease
    ("parse", "1.2.3-"),           # empty prerelease
    ("parse", "foobar"),
    # valid
    ("valid", "1.2.3"),
    ("valid", "1.2.3-rc.1+build"),
    ("valid", "1.2"),
    # the spec precedence chain (semver.org §11)
    ("cmp", "1.0.0|2.0.0"),
    ("cmp", "2.0.0|2.0.0"),
    ("cmp", "1.0.0-alpha|1.0.0"),
    ("cmp", "1.0.0-alpha|1.0.0-alpha.1"),
    ("cmp", "1.0.0-alpha.1|1.0.0-alpha.beta"),
    ("cmp", "1.0.0-alpha.beta|1.0.0-beta"),
    ("cmp", "1.0.0-beta|1.0.0-beta.2"),
    ("cmp", "1.0.0-beta.2|1.0.0-beta.11"),
    ("cmp", "1.0.0-beta.11|1.0.0-rc.1"),
    ("cmp", "1.0.0-rc.1|1.0.0"),
    ("cmp", "1.0.0+build.1|1.0.0+build.2"),   # build ignored in compare
    # match
    ("match", "2.0.0|>=1.0.0"),
    ("match", "1.0.0|>1.0.0"),
    ("match", "4.0.4|4.0.4"),
    ("match", "1.2.3|!=1.2.3"),
    ("match", "1.2.3|<=1.2.3"),
    ("match", "1.2.3|=1.2.3"),       # invalid operator -> error
    # bump
    ("bump", "major|1.2.3"),
    ("bump", "minor|1.2.3"),
    ("bump", "patch|1.2.3"),
    ("bump", "prerelease|1.2.3"),
    ("bump", "prerelease|1.2.3-rc.1"),
    ("bump", "prerelease|1.2.3-alpha"),
    ("bump", "build|1.2.3"),
    ("bump", "build|1.2.3-rc.1+build.9"),
    ("bump", "build|1.2.3+alpha"),
    # next_version
    ("next", "patch|1.2.3"),
    ("next", "minor|1.2.3"),
    ("next", "major|1.2.3"),
    ("next", "prerelease|1.2.3"),
    ("next", "prerelease|1.2.3-rc.1"),
    ("next", "patch|1.2.3-rc.1"),       # prerelease present -> finalize
    ("next", "prerelease|1.2.3-beta.1"),  # token rc != beta -> replace
    ("next", "build|1.2.3"),            # invalid part -> error
    # finalize
    ("finalize", "1.2.3-rc.5+b"),
    ("finalize", "1.2.3"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
