#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored ahocorapy KeywordTree and writes
expected.out.

  tree <0|1>  start a new KeywordTree(case_insensitive=bool(flag))
  kw   <word> tree.add(word)
  all  <text> finalize (first query); print " ".join("kw@start" for match)
  one  <text> finalize (first query); print "kw@start" or "None"

`tree`/`kw` print nothing. mini_ahocorasick.kara reproduces this byte-for-byte."""
import sys

sys.path.insert(0, "vendor")
from ahocorapy.keywordtree import KeywordTree  # noqa: E402

tree = None
finalized = False
out = []

for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "tree":
        tree = KeywordTree(case_insensitive=(arg == "1"))
        finalized = False
    elif op == "kw":
        tree.add(arg)
    elif op in ("all", "one"):
        if not finalized:
            tree.finalize()
            finalized = True
        matches = list(tree.search_all(arg))
        if op == "all":
            out.append(" ".join("%s@%d" % (kw, start) for kw, start in matches))
        else:
            if matches:
                kw, start = matches[0]
                out.append("%s@%d" % (kw, start))
            else:
                out.append("None")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
