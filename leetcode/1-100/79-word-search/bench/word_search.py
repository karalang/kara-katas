"""Benchmark workload — Word Search (LeetCode #79).

Python mirror of bench/word_search.kara. Enumerates every self-avoiding walk (up to
`depth` steps) from every start cell of a fixed all-'A' 5x5 board and folds each
visited cell into a threaded accumulator — the 4-neighbour, in-place mark/restore DFS
backtracking that powers word search, with the letter-match replaced by "any
unvisited cell, up to depth" so every branch is taken. Runs a smaller K (pure-Python
recursion is slow at full scale); timed separately, NOT cross-checked. See
../README.md.
"""

import sys

ROWS = 5
COLS = 5


def walk(board, r, c, depth, acc):
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return acc
    if board[r][c] == 0:
        return acc
    a = (acc * 131 + (r * COLS + c) + 1) % 1000000007
    if depth == 0:
        return a
    saved = board[r][c]
    board[r][c] = 0
    a = walk(board, r + 1, c, depth - 1, a)
    a = walk(board, r - 1, c, depth - 1, a)
    a = walk(board, r, c + 1, depth - 1, a)
    a = walk(board, r, c - 1, depth - 1, a)
    board[r][c] = saved
    return a


def search_all(board, depth, seed):
    a = seed
    for r in range(ROWS):
        for c in range(COLS):
            a = walk(board, r, c, depth, a)
    return a


def main():
    depth = 25
    total = 2
    modulus = 1000000007
    board = [[ord('A')] * COLS for _ in range(ROWS)]
    total_sum = 0
    for it in range(total):
        rr = search_all(board, depth, it)
        total_sum = (total_sum + rr) % modulus
    print(total_sum)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
