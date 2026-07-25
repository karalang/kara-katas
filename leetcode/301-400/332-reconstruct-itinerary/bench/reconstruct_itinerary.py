"""Benchmark harness for LeetCode #332 — Hierholzer Eulerian path.

Mirrors reconstruct_itinerary.kara algorithm-for-algorithm.

NOTE: the adjacency build uses setdefault(...).append(...), which is O(1)
amortized. The Kara mirror cannot express that — m[k].push(x) is rejected by
codegen (kara ledger B-2026-07-25-5, open) — so it does get-copy-push-insert at
O(degree) per edge. See ../README.md § Benchmarks.
"""

import sys

M = 40
L = 24
ITERS = 250

# The walk recurses once per edge; 1000 edges exceeds the default limit of 1000.
sys.setrecursionlimit(100000)


def visit(adj, cursor, airport, route):
    while True:
        used = cursor.get(airport, 0)
        d = adj.get(airport)
        if d is None or used >= len(d):
            break
        nxt = d[used]
        cursor[airport] = used + 1
        visit(adj, cursor, nxt, route)
    route.append(airport)


def find_itinerary(froms, tos, rot):
    e = len(froms)
    adj = {}
    for i in range(e):
        idx = (i + rot) % e
        adj.setdefault(froms[idx], []).append(tos[idx])

    for d in adj.values():
        d.sort()

    cursor = {}
    route = []
    visit(adj, cursor, "JFK", route)
    route.reverse()
    return route


def main():
    froms = []
    tos = []
    for j in range(M):
        prev = "JFK"
        for k in range(L):
            cur = f"A{j * L + k}"
            froms.append(prev)
            tos.append(cur)
            prev = cur
        froms.append(prev)
        tos.append("JFK")

    sink = 0
    for it in range(ITERS):
        path = find_itinerary(froms, tos, it)
        for i, s in enumerate(path):
            cs = sum(s.encode())
            sink += (i + 1) * cs
    print(sink)


if __name__ == "__main__":
    main()
