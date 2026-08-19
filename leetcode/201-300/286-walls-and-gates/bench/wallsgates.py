#!/usr/bin/env python3
"""Python mirror of wallsgates_seq.kara — see ../README.md § Benchmarks.

Same LCG, same board parameters, same flat queue, same build-once/punch-many
shape. Kept structurally identical to the compiled mirrors rather than rewritten
in a more Pythonic style, because the point is to time the same algorithm.
"""

INF = 2147483647


def make_board(b, n):
    g = []
    s = 777 + b * 1013
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        roll = s % 100
        g.append(-1 if roll < 20 else 0 if roll < 21 else INF)
    return g


def solve(template, r, c):
    n = r * c
    g = list(template)

    q = [k for k in range(n) if g[k] == 0]

    head = 0
    while head < len(q):
        cell = q[head]
        head += 1
        row, col = divmod(cell, c)
        d = g[cell] + 1
        if row > 0:
            nb = cell - c
            if g[nb] == INF:
                g[nb] = d
                q.append(nb)
        if row < r - 1:
            nb = cell + c
            if g[nb] == INF:
                g[nb] = d
                q.append(nb)
        if col > 0:
            nb = cell - 1
            if g[nb] == INF:
                g[nb] = d
                q.append(nb)
        if col < c - 1:
            nb = cell + 1
            if g[nb] == INF:
                g[nb] = d
                q.append(nb)

    total = 0
    unreachable = 0
    for v in g:
        if v == INF:
            unreachable += 1
        elif v > 0:
            total += v
    return total, unreachable


def run_board(b, r, c, reps):
    template = make_board(b, r * c)
    total = unreachable = 0
    for _ in range(reps):
        t, u = solve(template, r, c)
        total += t
        unreachable += u
    return total, unreachable


def main():
    boards, r, c, reps = 16, 512, 512, 8
    total = unreachable = 0
    for b in range(boards):
        t, u = run_board(b, r, c, reps)
        total += t
        unreachable += u
    print(total, unreachable)


main()
