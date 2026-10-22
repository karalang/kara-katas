#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored `astar` library and writes
expected.out.

  grid <w> <h> <cells>       build a Maze(AStar) over the w*h grid
  path <sr> <sc> <gr> <gc>   Maze.astar(start, goal); print the path

A node is encoded as r*w + c. The Maze subclass supplies the Manhattan
heuristic, unit step cost, and 4-neighbours in the order up, left, right, down
(walls and out-of-bounds skipped). A path prints as `r,c` cells joined by
`->`, or `no path`. mini_astar.kara reproduces this byte-for-byte."""
import sys

sys.path.insert(0, "vendor")
from astar import AStar  # noqa: E402


class Maze(AStar):
    def __init__(self, grid, w, h):
        self.grid = grid
        self.w = w
        self.h = h

    def heuristic_cost_estimate(self, a, b):
        ar, ac = divmod(a, self.w)
        br, bc = divmod(b, self.w)
        return abs(ar - br) + abs(ac - bc)

    def distance_between(self, n1, n2):
        return 1

    def neighbors(self, node):
        r, c = divmod(node, self.w)
        out = []
        for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.h and 0 <= nc < self.w and self.grid[nr * self.w + nc] == 0:
                out.append(nr * self.w + nc)
        return out


grid = None
w = h = 0
out = []

for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "grid":
        ws, hs, cells = arg.split(" ")
        w, h = int(ws), int(hs)
        grid = [1 if ch == "#" else 0 for ch in cells]
    elif op == "path":
        sr, sc, gr, gc = (int(x) for x in arg.split(" "))
        start, goal = sr * w + sc, gr * w + gc
        if grid[start] == 1 or grid[goal] == 1:
            out.append("no path")
            continue
        res = Maze(grid, w, h).astar(start, goal)
        if res is None:
            out.append("no path")
        else:
            out.append("->".join("%d,%d" % divmod(n, w) for n in res))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
