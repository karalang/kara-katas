#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored snowballstemmer Porter stemmer
and writes expected.out.

  stem <word>  -> PorterStemmer.stemWord(word)

mini_snowball.kara reproduces this byte-for-byte on every backend."""
import sys

sys.path.insert(0, "vendor")
import snowballstemmer  # noqa: E402

st = snowballstemmer.stemmer("porter")

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "stem":
        out.append(st.stemWord(arg))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
