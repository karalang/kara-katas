#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_specifiers: one job per line, `op \t args...`.

Two ops, both the heart of pip's dependency resolution — "does this version
satisfy this requirement?" (`contains`) and "which of these versions do?"
(`filter`):

  contains \t <specifier-set> \t <version> \t <premode>
  filter   \t <specifier-set> \t <premode> \t <v1,v2,...>

<premode> is none|true|false — the `prereleases=` argument (None autodetects
per PEP 440). The jobs exercise every operator (>= <= > < == != ~= ===), the
`==V.*` / `!=V.*` wildcards, epochs, the `<V`/`>V` pre/post carve-outs,
multi-clause sets, the pre-release acceptance rules, and the PEP 440 filter
buffering (pre-releases are yielded only when no final release matches).
"""
import os

# Each spec-set is checked against a battery of versions under each premode.
CONTAINS = [
    # >= : lower-inclusive, and a prerelease above the bound matches by default.
    (">=1.2.3", ["1.2.3", "1.2.2", "1.3", "2.0", "1.3.0a1", "1.2.3a1"], "none"),
    (">=1.2.3", ["1.3.0a1"], "false"),
    # <= : upper-inclusive.
    ("<=2.0", ["2.0", "2.0.0", "2.0.1", "1.9", "2.0a1"], "none"),
    # < : excludes the bound and its own pre-releases.
    ("<1.0", ["0.9", "1.0", "1.0a1", "1.0.dev1", "0.9.9"], "none"),
    ("<1.0a2", ["1.0a1", "1.0a2", "0.9"], "none"),
    # > : excludes the bound and its post-releases.
    (">1.0", ["1.0", "1.0.post1", "1.0.1", "1.1", "2.0"], "none"),
    (">1.0.post1", ["1.0.post1", "1.0.post2", "1.1"], "none"),
    # == exact (release-zero-insensitive) and != .
    ("==1.2.3", ["1.2.3", "1.2.3.0", "1.2.3.1", "1.2"], "none"),
    ("!=1.2.3", ["1.2.3", "1.2.4", "1.2.3.0"], "none"),
    # == wildcard / != wildcard (prefix match on the release).
    ("==1.2.*", ["1.2", "1.2.5", "1.3", "1.1.9", "1.2.0"], "none"),
    ("!=1.4.*", ["1.4", "1.4.7", "1.5", "1.3.9"], "none"),
    # ~= compatible release.
    ("~=2.2", ["2.2", "2.5", "3.0", "2.1", "2.2.9"], "none"),
    ("~=1.4.5", ["1.4.5", "1.4.9", "1.5", "1.4.4", "1.5.0"], "none"),
    # === arbitrary string identity (case-insensitive, unparsed).
    ("===1.0.0", ["1.0.0", "1.0", "1.0.0+local", "foobar"], "none"),
    ("===foobar", ["foobar", "FOOBAR", "foo"], "none"),
    # epochs: an epoch outranks everything without one.
    ("==2!1.0", ["2!1.0", "1.0", "2!1.0.0"], "none"),
    (">=1!0", ["1!0", "99", "1!0.1"], "none"),
    # pre-release spec: naming a prerelease opts the whole spec into pre mode.
    (">=1.0b2", ["1.0b2", "1.0rc1", "1.0", "1.0b1", "1.0a9"], "none"),
    # multi-clause sets (intersection).
    (">=1.0,<2.0", ["1.0", "1.5", "2.0", "0.9", "1.9.9"], "none"),
    (">=1.0,!=1.5,<2.0", ["1.4", "1.5", "1.6", "2.0"], "none"),
    ("~=1.4,!=1.4.5", ["1.4.0", "1.4.5", "1.4.6", "1.5"], "none"),
    (">=1.0,<2.0", ["1.5a1"], "none"),
    (">=1.0,<2.0", ["1.5a1"], "true"),
    (">=1.0,<2.0", ["1.5a1"], "false"),
    # empty set accepts everything (default pre-release rule still applies).
    ("", ["1.0", "2.0a1", "lolwat"], "none"),
    # normalization of alternate version spellings in the input.
    ("==1.0", ["1.0.0", "1!1.0", "v1.0"], "none"),
    (">1.0a1", ["1.0alpha2", "1.0a1", "1.0c1", "1.0preview1"], "none"),
    # unparsable inputs never match a standard operator.
    (">=1.0", ["lolwat", "1..2", ""], "none"),
]

# filter: order-preserving, with PEP 440 pre-release buffering under `none`.
FILTER = [
    (">=1.2.3", "none", ["1.2", "1.3", "1.5a1"]),
    (">=1.2.3", "none", ["1.2", "1.5a1"]),
    (">=1.2.3", "true", ["1.3", "1.5a1"]),
    (">=1.2.3", "false", ["1.3", "1.5a1", "1.4"]),
    (">=1.0,<2.0", "none", ["0.9", "1.0", "1.5", "1.9", "2.0", "1.7b1"]),
    ("~=1.4", "none", ["1.3", "1.4", "1.4.9", "1.5", "2.0"]),
    ("==1.2.*", "none", ["1.1", "1.2", "1.2.9", "1.3", "1.2a1"]),
    (">=2.0b1", "none", ["2.0a1", "2.0b1", "2.0b2", "2.0", "1.9"]),
    ("", "none", ["1.3", "1.5a1"]),
    ("", "true", ["1.3", "1.5a1"]),
    ("", "false", ["1.3", "1.5a1"]),
    ("!=1.5", "none", ["1.4", "1.5", "1.6", "1.5a1"]),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for spec, versions, pre in CONTAINS:
        for v in versions:
            fh.write("contains\t" + spec + "\t" + v + "\t" + pre + "\n")
    for spec, pre, versions in FILTER:
        fh.write("filter\t" + spec + "\t" + pre + "\t" + ",".join(versions) + "\n")
