#!/usr/bin/env python3
"""Writes data/jobs.tsv: the job list that both oracle.py and the Kara port
run through packaging's PEP 440 Version and the name/version canonicalizers.

A job is one line of tab-separated fields; field 0 names the kind:
  parse  <v>            round-trip str(Version(v)), or the InvalidVersion message
  props  <v>            every attribute of a Version
  cmp    <a> <b>        the six comparison operators on two versions
  sort   <v,v,...>      the versions sorted ascending, as their strings
  cname  <name>         canonicalize_name
  cver   <v> <0|1>      canonicalize_version, strip_trailing_zero = the flag
"""
import os

os.makedirs("data", exist_ok=True)

JOBS = r"""
parse	1
parse	1.0
parse	1.0.0
parse	1.2.3
parse	1.0.0.0.0
parse	v1.2.3
parse	1!2.0
parse	1.0a1
parse	1.0alpha1
parse	1.0-a.1
parse	1.0a
parse	1.0.a.4
parse	1.0b2
parse	1.0beta2
parse	1.0rc1
parse	1.0c1
parse	1.0pre5
parse	1.0preview5
parse	1.0.post1
parse	1.0-1
parse	1.0rev2
parse	1.0r3
parse	1.0.post
parse	1.0.dev1
parse	1.0dev
parse	1.0.dev
parse	1.0+abc.1.twelve
parse	1.0+Ubuntu-1
parse	1!2.0.0a1.post2.dev3+foo.bar.5
parse	01.002.03
parse	2016.07
parse	invalid
parse	1..2
parse	.1
parse	1.0.0+
parse	1.2.3.
parse	1.0++
parse
props	1.2.3
props	1!2.0.0a1.post2.dev3+foo.1
props	1.0
props	2.0.0.0
props	1.0rc2
props	1.0.post4
props	1.0.dev7
props	5
cmp	1.0	1.0.0
cmp	1.0	1.0.1
cmp	1.0a1	1.0
cmp	1.0.dev1	1.0a1
cmp	1.0a1	1.0b1
cmp	1.0rc1	1.0
cmp	1.0	1.0.post1
cmp	1.0.post1	1.0.post2
cmp	1!1.0	2.0
cmp	1.0+local	1.0
cmp	1.0+abc	1.0+abd
cmp	1.0+1	1.0+2
cmp	1.0.0	1.0
cmp	1.0a2	1.0a10
cmp	1.0.dev1	1.0.dev1
sort	1.0,1.0.dev1,1.0a1,1.0b2,1.0rc1,1.0.post1,1.1,1!0.1,2.0.dev0
sort	1.0+2,1.0+1,1.0+10,1.0,1.0+1.1
sort	2.0,1.0,1.5,1.0.1,1.0.0
cname	Django
cname	oslo.concurrency
cname	requests
cname	A__B--C.._D
cname	Flask-SQLAlchemy
cver	1.0.1	1
cver	1.0.0	1
cver	1.0.0	0
cver	1.4.0.0.0	1
cver	1!2.0.0	1
cver	1.0a1.post2	1
cver	foo bar baz	1
cver	2.0	0
"""

with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))

print("jobs:", len(JOBS.strip().splitlines()))
