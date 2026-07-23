"""Benchmark workload for LeetCode #212 — Word Search II (Python; scale lane)."""

import sys

ALPHA = 6
SIZE = 12


def dfs(board, children, is_end, r, c, node):
    cell = board[r * SIZE + c]
    if cell == -1:
        return 0
    nxt = children[node * ALPHA + cell]
    if nxt == 0:
        return 0
    cnt = nxt  # checksum each descended node
    if is_end[nxt] == 1:
        is_end[nxt] = 0  # collect each word once per run
        cnt += nxt  # + collected-word identity
    board[r * SIZE + c] = -1  # mark visited
    if r > 0:
        cnt += dfs(board, children, is_end, r - 1, c, nxt)
    if r + 1 < SIZE:
        cnt += dfs(board, children, is_end, r + 1, c, nxt)
    if c > 0:
        cnt += dfs(board, children, is_end, r, c - 1, nxt)
    if c + 1 < SIZE:
        cnt += dfs(board, children, is_end, r, c + 1, nxt)
    board[r * SIZE + c] = cell  # restore
    return cnt


def main():
    nwords = 4000
    runs = 40000
    cells = SIZE * SIZE

    children = [0] * ALPHA  # root at index 0
    is_end0 = [0]

    state = 12345

    # Build trie once.
    for _ in range(nwords):
        state = (state * 1103515245 + 12345) & 2147483647
        length = 5 + state % 4  # 5..8
        cur = 0
        for _ in range(length):
            state = (state * 1103515245 + 12345) & 2147483647
            ch = state % ALPHA
            nxt = children[cur * ALPHA + ch]
            if nxt == 0:
                idx = len(is_end0)
                children.extend([0] * ALPHA)
                is_end0.append(0)
                children[cur * ALPHA + ch] = idx
                cur = idx
            else:
                cur = nxt
        is_end0[cur] = 1

    nnodes = len(is_end0)
    board = [0] * cells

    sink = 0
    for _ in range(runs):
        is_end = is_end0[:]  # restore word-end flags
        # Fresh board each run from the ongoing PRNG stream.
        for bi in range(cells):
            state = (state * 1103515245 + 12345) & 2147483647
            board[bi] = state % ALPHA
        found = 0
        for r in range(SIZE):
            for c in range(SIZE):
                found += dfs(board, children, is_end, r, c, 0)
        sink += found

    print(sink)


sys.setrecursionlimit(100000)
main()
