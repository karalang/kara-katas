"""Benchmark workload for LeetCode #211 — Add and Search Words Data Structure (Python; scale lane)."""

import sys

ALPHA = 6
WLEN = 6


def dfs(children, is_end, wild, letter, cur, pos):
    if pos == WLEN:
        return is_end[cur] == 1
    if wild[pos] == 1:
        for a in range(ALPHA):
            nc = children[cur * ALPHA + a]
            if nc != 0 and dfs(children, is_end, wild, letter, nc, pos + 1):
                return True
        return False
    nc = children[cur * ALPHA + letter[pos]]
    if nc == 0:
        return False
    return dfs(children, is_end, wild, letter, nc, pos + 1)


def main():
    nwords = 20000
    nquery = 8000000

    children = [0] * ALPHA  # root at index 0
    is_end = [0]

    state = 12345

    # Build phase.
    for _ in range(nwords):
        cur = 0
        for _ in range(WLEN):
            state = (state * 1103515245 + 12345) & 2147483647
            c = state % ALPHA
            nxt = children[cur * ALPHA + c]
            if nxt == 0:
                idx = len(is_end)
                children.extend([0] * ALPHA)
                is_end.append(0)
                children[cur * ALPHA + c] = idx
                cur = idx
            else:
                cur = nxt
        is_end[cur] = 1

    # Query phase.
    wild = [0] * WLEN
    letter = [0] * WLEN
    sink = 0
    for _ in range(nquery):
        for k in range(WLEN):
            state = (state * 1103515245 + 12345) & 2147483647
            v = state
            wild[k] = 1 if v % 6 == 0 else 0
            letter[k] = (v // 6) % ALPHA
        if dfs(children, is_end, wild, letter, 0, 0):
            sink += 1

    print(sink)


sys.setrecursionlimit(100)
main()
