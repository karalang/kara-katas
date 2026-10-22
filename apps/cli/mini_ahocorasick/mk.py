#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_ahocorasick (tab-separated: op then arg).

A stream of Aho-Corasick keyword trees, each built then queried, in order:
  tree <0|1>  start a new tree (0 = case-sensitive, 1 = case-insensitive)
  kw   <word> add a keyword to the current tree
  all  <text> finalize (first query) and search_all; print every match
  one  <text> search_one; print the first match, or None

`tree` and `kw` print nothing; `all`/`one` each print one line. A match is
rendered `keyword@startindex`; `all` joins its matches with spaces (empty line
if none), `one` prints one match or `None`. Start indices are byte offsets
(= character offsets for the ASCII inputs used here).

mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored ahocorapy library. Keys and texts are ASCII. See
README.md."""
import os

os.makedirs("data", exist_ok=True)

# (case_insensitive, [keywords], [("all"|"one", text), ...])
TREES = [
    # the classic he/she/his/hers automaton
    (0, ["he", "she", "his", "hers"],
     [("all", "ushers"), ("all", "hishers"), ("all", "she said he is here"),
      ("all", "xyz"), ("all", ""), ("one", "ushers"), ("one", "zzz"),
      ("all", "h"), ("all", "hhhh")]),
    # overlapping / repeated symbols
    (0, ["aa", "aaa", "aba"],
     [("all", "aaaaa"), ("all", "ababa"), ("all", "abaaab"), ("one", "aaaaa"),
      ("all", "b"), ("all", "aabaa")]),
    # case-insensitive brand/language scanner over mixed-case prose
    (1, ["python", "java", "go", "rust", "c"],
     [("all", "I love Python and JAVA and Go and rUsT"),
      ("all", "gogogo"), ("one", "PYTHONISTA"), ("all", "C C++ and C#"),
      ("all", "no languages here"), ("one", "scala")]),
    # log-level keywords (prefix-overlapping warn/warning, fail/failure)
    (0, ["error", "warn", "warning", "fail", "failure", "ok"],
     [("all", "error: disk warning, task failure then ok"),
      ("all", "warnwarning"), ("all", "failfailure"),
      ("one", "all systems ok"), ("all", "no issues"),
      ("all", "ERROR")]),
    # mississippi: suffix-overlapping needles
    (0, ["issi", "ssi", "sip", "mississippi", "is", "pi"],
     [("all", "mississippi"), ("all", "the mississippi river is wide"),
      ("one", "mississippi"), ("all", "sipissi"), ("all", "pip")]),
    # single-character and whole-word keywords mixed
    (0, ["a", "an", "and", "band", "candy"],
     [("all", "a band and a candy"), ("all", "andandand"),
      ("one", "candy"), ("all", "zzz")]),
]

lines = []
for ci, kws, queries in TREES:
    lines.append("tree\t%d" % ci)
    for k in kws:
        lines.append("kw\t%s" % k)
    for op, text in queries:
        lines.append("%s\t%s" % (op, text))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
