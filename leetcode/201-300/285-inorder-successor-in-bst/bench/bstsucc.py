#!/usr/bin/env python3
"""LeetCode 285 bench mirror — Python. Same arena, descent and sink."""
N = 300000
QUERIES = 2000000
key, lft, rgt = [0]*N, [0]*N, [0]*N
cnt = 0


def insert(k):
    global cnt
    if cnt == 0:
        key[0], lft[0], rgt[0] = k, -1, -1
        cnt = 1
        return
    cur = 0
    while True:
        if k < key[cur]:
            if lft[cur] < 0:
                key[cnt], lft[cnt], rgt[cnt] = k, -1, -1
                lft[cur] = cnt
                cnt += 1
                return
            cur = lft[cur]
        else:
            if rgt[cur] < 0:
                key[cnt], lft[cnt], rgt[cnt] = k, -1, -1
                rgt[cur] = cnt
                cnt += 1
                return
            cur = rgt[cur]


def successor(target):
    if cnt == 0:
        return None
    cur, best = 0, None
    while cur >= 0:
        if key[cur] > target:
            best = key[cur]
            cur = lft[cur]
        else:
            cur = rgt[cur]
    return best


def main():
    seed = 20260825
    for _ in range(N):
        seed = (seed * 1103515245 + 12345) % 2147483648
        insert(seed % 1000000)
    sink = found = 0
    for _ in range(QUERIES):
        seed = (seed * 1103515245 + 12345) % 2147483648
        s = successor(seed % 1000000)
        if s is not None:
            found += 1
        sink = (sink * 31 + (s if s is not None else -1)) % 1000000007
    print(sink, found)


main()
