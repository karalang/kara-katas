#!/usr/bin/env python3
"""Python mirror of differential.kara — the same grids, the same four solvers.

Run both and diff the output; they must agree line for line. The Kara harness is
the artifact under test, and this file exists so a disagreement can be blamed on
one side rather than argued about.

Everything here mirrors the Kara source structurally: the same LCG, the same grid
shapes in the same order, the same solvers with the same relaxation accounting.
"""

from collections import deque

INF = 2147483647


# ---- the shared generator ---------------------------------------------------

class Rng:
    """The LCG both harnesses run. Identical constants, identical sequence."""

    def __init__(self, seed):
        self.s = seed

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s

    def below(self, n):
        return self.next() % n


def trunc_mod(a, n):
    """`a % n` with KARA's sign rule, which is not Python's.

    Kara's `%` truncates toward zero, like C, Rust and Go: `-1 % 1000` is `-1`.
    Python's floors: `-1 % 1000` is `999`. Every other number this harness prints
    agreed across the two mirrors on the first run; the digest did not, because it
    is the only one that hashes a wall (`-1`) rather than a distance. Writing the
    Kara rule out here rather than "fixing" the digest keeps the mirror a mirror —
    Kara is the artifact under test, so Python is the side that has to bend.
    """
    return abs(a) % n * (1 if a >= 0 else -1)


def make_grid(rng, r, c, shape):
    """One grid. `shape` picks the wall/gate mix — see differential.kara."""
    if shape == 0:      # ordinary: some walls, a few gates
        wall_pct, gate_pct = 25, 12
    elif shape == 1:    # maze: dense walls, scarce gates -> unreachable rooms
        wall_pct, gate_pct = 45, 5
    else:               # gate-rich: many sources, short distances
        wall_pct, gate_pct = 10, 30

    g = []
    for _ in range(r * c):
        roll = rng.below(100)
        if roll < wall_pct:
            g.append(-1)
        elif roll < wall_pct + gate_pct:
            g.append(0)
        else:
            g.append(INF)
    return g


# ---- solver 1: multi-source BFS (the star) ----------------------------------

def bfs(g, r, c):
    relax = 0
    q = deque(i for i in range(r * c) if g[i] == 0)
    while q:
        cell = q.popleft()
        d = g[cell] + 1
        row, col = divmod(cell, c)
        for ok, n in ((row > 0, cell - c), (row < r - 1, cell + c),
                      (col > 0, cell - 1), (col < c - 1, cell + 1)):
            if ok and g[n] == INF:
                g[n] = d
                relax += 1
                q.append(n)
    return relax


# ---- solver 2: the same BFS over a sum type ---------------------------------
#
# Python has no enums-with-payload worth the ceremony here, so the mirror keeps
# the tagged-tuple shape: ("wall",), ("reached", d), ("room",). The point of the
# Kara file is the type; the point of the mirror is the numbers.

def enum_solver(g, r, c):
    cells = [("wall",) if v == -1 else ("room",) if v == INF else ("reached", v)
             for v in g]
    relax = 0
    q = deque(i for i in range(r * c) if cells[i] == ("reached", 0))
    while q:
        cell = q.popleft()
        d = cells[cell][1] + 1
        row, col = divmod(cell, c)
        for ok, n in ((row > 0, cell - c), (row < r - 1, cell + c),
                      (col > 0, cell - 1), (col < c - 1, cell + 1)):
            if ok and cells[n] == ("room",):
                cells[n] = ("reached", d)
                relax += 1
                q.append(n)
    for i, cell in enumerate(cells):
        g[i] = -1 if cell[0] == "wall" else INF if cell[0] == "room" else cell[1]
    return relax


# ---- solver 3: DFS relaxation -----------------------------------------------

def dfs(g, r, c):
    relax = 0

    def flood(cell, d):
        nonlocal relax
        if g[cell] == -1 or g[cell] < d:
            return
        g[cell] = d
        relax += 1
        row, col = divmod(cell, c)
        for ok, n in ((row > 0, cell - c), (row < r - 1, cell + c),
                      (col > 0, cell - 1), (col < c - 1, cell + 1)):
            if ok:
                flood(n, d + 1)

    for i in range(r * c):
        if g[i] == 0:
            row, col = divmod(i, c)
            for ok, n in ((row > 0, i - c), (row < r - 1, i + c),
                          (col > 0, i - 1), (col < c - 1, i + 1)):
                if ok:
                    flood(n, 1)
    return relax


# ---- solver 4: one BFS per room (the definitional oracle) -------------------

def nearest_gate(g, r, c, start):
    seen = [False] * (r * c)
    seen[start] = True
    q = deque([(start, 0)])
    while q:
        cell, d = q.popleft()
        if g[cell] == 0:
            return d
        row, col = divmod(cell, c)
        for ok, n in ((row > 0, cell - c), (row < r - 1, cell + c),
                      (col > 0, cell - 1), (col < c - 1, cell + 1)):
            if ok and g[n] != -1 and not seen[n]:
                seen[n] = True
                q.append((n, d + 1))
    return INF


def brute(g, r, c):
    source = list(g)
    answers = [nearest_gate(source, r, c, i) if source[i] == INF else source[i]
               for i in range(r * c)]
    relax = 0
    for j in range(r * c):
        if source[j] == INF and answers[j] != INF:
            relax += 1
        g[j] = answers[j]
    return relax


# ---- the harness ------------------------------------------------------------

def main():
    rng = Rng(12345)

    grids = 0
    cells_total = 0
    bfs_bad = enum_bad = dfs_bad = 0
    relax_bad = 0
    grids_with_unreachable = 0
    unreachable_cells = 0
    bfs_relax_total = dfs_relax_total = 0
    digest = 0

    for shape in range(3):
        for r in range(1, 7):
            for c in range(1, 7):
                for _ in range(12):
                    g0 = make_grid(rng, r, c, shape)
                    grids += 1
                    cells_total += r * c

                    ref = list(g0)
                    ref_relax = brute(ref, r, c)

                    a = list(g0)
                    a_relax = bfs(a, r, c)
                    b = list(g0)
                    b_relax = enum_solver(b, r, c)
                    d = list(g0)
                    d_relax = dfs(d, r, c)

                    if a != ref:
                        bfs_bad += 1
                    if b != ref:
                        enum_bad += 1
                    if d != ref:
                        dfs_bad += 1

                    # The reachable-room count, straight off the oracle.
                    reachable = sum(1 for i in range(r * c)
                                    if g0[i] == INF and ref[i] != INF)

                    # BFS, the sum type and the oracle each write a reachable
                    # room exactly once. The DFS may write it several times, so
                    # it is only bounded below.
                    if (a_relax != reachable or b_relax != reachable
                            or ref_relax != reachable or d_relax < reachable):
                        relax_bad += 1

                    unreach = sum(1 for i in range(r * c) if ref[i] == INF and g0[i] == INF)
                    if unreach > 0:
                        grids_with_unreachable += 1
                    unreachable_cells += unreach

                    bfs_relax_total += a_relax
                    dfs_relax_total += d_relax

                    for v in ref:
                        digest = (digest * 31 + trunc_mod(v, 1000)) % 1000000007

    print(f"grids                {grids}")
    print(f"cells                {cells_total}")
    print(f"bfs disagreements    {bfs_bad}")
    print(f"enum disagreements   {enum_bad}")
    print(f"dfs disagreements    {dfs_bad}")
    print(f"relaxation violations {relax_bad}")
    print(f"grids w/ unreachable {grids_with_unreachable}")
    print(f"unreachable cells    {unreachable_cells}")
    print(f"bfs relaxations      {bfs_relax_total}")
    print(f"dfs relaxations      {dfs_relax_total}")
    print(f"digest               {digest}")


main()
