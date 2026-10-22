#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_astar (tab-separated: op then arg).

A stream of grid mazes, each defined then queried for shortest paths:
  grid <w> <h> <cells>   start a new maze; <cells> is a w*h row-major string
                         of '.' (open) and '#' (wall)
  path <sr> <sc> <gr> <gc>   find a shortest path from (sr,sc) to (gr,gc)

`grid` prints nothing. `path` prints the path as `r,c` cells joined by `->`
(just `sr,sc` when start == goal), or `no path` when the goal is unreachable
or either endpoint is a wall. The path is the A* result: a shortest path, with
ties broken by neighbor order (up, left, right, down) and heapq's pop order —
so mazes with several equally short paths pin exactly one.

mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored `astar` library. All inputs are ASCII. See README.md."""
import os

os.makedirs("data", exist_ok=True)

# (w, h, [row, row, ...], [(sr, sc, gr, gc), ...])
MAZES = [
    # wide-open 5x5: many equal-cost paths -> stresses tie-breaking
    (5, 5,
     [".....",
      ".....",
      ".....",
      ".....",
      "....."],
     [(0, 0, 4, 4), (0, 4, 4, 0), (2, 2, 2, 2), (0, 0, 0, 4), (4, 4, 0, 0)]),
    # corridor maze: a single forced route
    (7, 5,
     ["#######",
      "#.....#",
      "#####.#",
      "#.....#",
      "#.#####"],
     [(1, 1, 3, 1), (1, 1, 3, 5), (3, 1, 1, 5)]),
    # a room split by a wall with one gap
    (7, 7,
     [".......",
      ".......",
      ".......",
      "###.###",
      ".......",
      ".......",
      "......."],
     [(0, 0, 6, 6), (0, 6, 6, 0), (2, 0, 4, 6)]),
    # goal walled off -> no path
    (5, 5,
     [".....",
      ".###.",
      ".#.#.",
      ".###.",
      "....."],
     [(0, 0, 2, 2), (2, 2, 0, 0), (0, 0, 4, 4)]),
    # endpoints on walls, and start == goal
    (4, 4,
     ["....",
      ".##.",
      ".##.",
      "...."],
     [(1, 1, 0, 0), (0, 0, 1, 1), (3, 3, 3, 3), (0, 0, 3, 3)]),
    # degenerate shapes: 1xN and Nx1
    (5, 1,
     ["..#.."],
     [(0, 0, 0, 1), (0, 0, 0, 4), (0, 1, 0, 0)]),
    (1, 5,
     [".", ".", "#", ".", "."],
     [(0, 0, 1, 0), (0, 0, 4, 0), (3, 0, 4, 0)]),
    # a spiral-ish 8x8 with a longer detour
    (8, 8,
     ["........",
      ".######.",
      ".#....#.",
      ".#.##.#.",
      ".#.#..#.",
      ".#.####.",
      ".#......",
      ".#######"],
     [(0, 0, 4, 4), (0, 0, 6, 7), (4, 4, 0, 0), (0, 7, 6, 2)]),
]

lines = []
for w, h, rows, queries in MAZES:
    cells = "".join(rows)
    assert len(cells) == w * h, (w, h, len(cells))
    lines.append("grid\t%d %d %s" % (w, h, cells))
    for sr, sc, gr, gc in queries:
        lines.append("path\t%d %d %d %d" % (sr, sc, gr, gc))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
