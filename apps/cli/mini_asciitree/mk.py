#!/usr/bin/env python3
r"""Writes data/jobs.tsv: a sequence of trees to render, one node per line, as
three tab-separated fields `<style>\t<depth>\t<label>`. A depth-0 line starts a
new block (and carries that block's drawing style); the lines after it, until
the next depth-0 line, are its descendants, each attached to the most recent
line of smaller depth. No library import here — the inputs are literal."""

# (style, [(depth, label), ...]); depth 0 is the root. Styles: ascii (the
# library default +-|+), light/heavy/double (single-codepoint box glyphs),
# blank (indentation only), legacy (the "  +--" ASCII form).
BLOCKS = [
    ("ascii", [(0, "root"), (1, "sub1"), (2, "leaf1"), (2, "leaf2"),
               (1, "sub2"), (2, "leaf3"), (1, "sub3")]),
    ("light", [(0, "asciitree"), (1, "sometimes"), (2, "you"), (2, "just"),
               (1, "want"), (2, "to"), (2, "draw"), (3, "trees"), (1, "in"),
               (1, "your"), (1, "terminal")]),
    ("heavy", [(0, "P"), (1, "A"), (2, "B"), (2, "C"), (1, "D")]),
    ("double", [(0, "/"), (1, "etc"), (2, "nginx"), (3, "nginx.conf"),
                (2, "hosts"), (1, "home"), (2, "alice"), (2, "bob"),
                (1, "var"), (2, "log")]),
    ("blank", [(0, "root"), (1, "a"), (2, "aa"), (1, "b")]),
    ("legacy", [(0, "root"), (1, "sub1"), (2, "leaf1"), (2, "leaf2"),
                (1, "sub2"), (2, "leaf3")]),
    ("ascii", [(0, "single")]),
    ("ascii", [(0, "r"), (1, "only-child"), (2, "grand")]),
    ("light", [(0, "deep"), (1, "l1"), (2, "l2"), (3, "l3"), (4, "l4"),
               (1, "sibling")]),
    ("ascii", [(0, "Filesystem"), (1, "bin"), (1, "boot"), (2, "grub"),
               (1, "dev"), (1, "etc"), (2, "init.d"), (2, "rc.d"),
               (3, "rc.local"), (1, "usr"), (2, "bin"), (2, "lib"),
               (2, "local"), (3, "bin"), (1, "var"), (2, "log"),
               (3, "syslog"), (2, "tmp")]),
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    out = []
    for (style, nodes) in BLOCKS:
        for (depth, label) in nodes:
            out.append("%s\t%d\t%s" % (style, depth, label))
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


main()
