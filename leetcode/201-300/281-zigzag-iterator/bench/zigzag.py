#!/usr/bin/env python3
"""LeetCode 281 bench mirror — Python. Same cursor iterator, same skip scan."""
K = 64
ROUNDS = 2200


def drain_sink(lists):
    cursor = [0] * K
    remaining = sum(len(v) for v in lists)
    turn = tried = 0
    while tried < K and cursor[turn] >= len(lists[turn]):
        turn = (turn + 1) % K
        tried += 1
    h, pos = 0, 1
    while remaining > 0:
        t = turn
        v = lists[t][cursor[t]]
        cursor[t] += 1
        remaining -= 1
        h = (h * 31 + v * pos) % 1000000007
        pos += 1
        turn = (t + 1) % K
        scan = 0
        while scan < K and cursor[turn] >= len(lists[turn]):
            turn = (turn + 1) % K
            scan += 1
    return h


def main():
    seed = 20260819
    lists = []
    for _ in range(K):
        seed = (seed * 1103515245 + 12345) % 2147483648
        ln = 1 + (seed // 7) % 2000
        v = []
        for _ in range(ln):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v.append(seed % 100003)
        lists.append(v)
    sink = 0
    for _ in range(ROUNDS):
        sink = (sink + drain_sink(lists)) % 1000000007
    print(sink)


main()
