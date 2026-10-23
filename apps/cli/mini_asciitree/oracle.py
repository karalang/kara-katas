#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored asciitree library and writes
expected.out. Each block (a depth-0 line and its descendants) is rebuilt as the
nested ordered dict asciitree expects, rendered with the block's style, and
printed under a `=== block <n> (<style>) ===` header. mini_asciitree.kara
reproduces this byte-for-byte on every backend. The render walks the tree in
build order only (never over hash-map order), so the output is deterministic."""
import sys

sys.path.insert(0, "vendor")
import asciitree  # noqa: E402
from asciitree.drawing import (  # noqa: E402
    BoxStyle, BOX_ASCII, BOX_LIGHT, BOX_HEAVY, BOX_DOUBLE, BOX_BLANK,
)

GFX = {"ascii": BOX_ASCII, "light": BOX_LIGHT, "heavy": BOX_HEAVY,
       "double": BOX_DOUBLE, "blank": BOX_BLANK}


def drawer(style):
    if style == "legacy":
        return asciitree.LeftAligned(draw=asciitree.LegacyStyle())
    return asciitree.LeftAligned(draw=BoxStyle(gfx=GFX[style]))


def render_block(style, nodes):
    # nodes: list of (depth, label); build the nested dict honoring order.
    root_label = nodes[0][1]
    root = {}
    stack = [(0, root)]
    for (depth, label) in nodes[1:]:
        while stack and stack[-1][0] >= depth:
            stack.pop()
        d = {}
        stack[-1][1][label] = d
        stack.append((depth, d))
    return drawer(style)({root_label: root})


def main():
    blocks = []
    cur = None
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        style, depth_s, label = line.split("\t")
        depth = int(depth_s)
        if depth == 0:
            cur = (style, [])
            blocks.append(cur)
        cur[1].append((depth, label))
    out = []
    for n, (style, nodes) in enumerate(blocks):
        out.append("=== block %d (%s) ===" % (n, style))
        out.append(render_block(style, nodes))
    sys.stdout.write("\n".join(out) + "\n")


main()
