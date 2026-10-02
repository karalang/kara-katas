"""Benchmark workload for LeetCode #329 — Python mirror of
longest_increasing_path.kara.

Same workload: a SIDE x SIDE grid built once, then PUNCHES punches, each
replacing one cell and finding the longest increasing path again with a
fresh memo.
"""
import sys

sys.setrecursionlimit(1000000)

SIDE = 500
PUNCHES = 20
MODULUS = 1073741789
STEPS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def longest_from(matrix, memo, r, c):
    if memo[r][c] > 0:
        return memo[r][c]
    rows, cols = len(matrix), len(matrix[0])
    here = matrix[r][c]
    best = 1
    for dr, dc in STEPS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > here:
            length = 1 + longest_from(matrix, memo, nr, nc)
            if length > best:
                best = length
    memo[r][c] = best
    return best


def longest_increasing_path(matrix):
    if not matrix or not matrix[0]:
        return 0
    memo = [[0] * len(row) for row in matrix]
    best = 0
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            length = longest_from(matrix, memo, r, c)
            if length > best:
                best = length
    return best


seed = 329


def next_rand():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grid = [[next_rand() % 1000 for _ in range(SIDE)] for _ in range(SIDE)]
    sink = 0
    for _ in range(PUNCHES):
        r = next_rand() % SIDE
        c = next_rand() % SIDE
        grid[r][c] = next_rand() % 1000
        length = longest_increasing_path(grid)
        sink = (sink * 31 + length * 1000003 + r * SIDE + c) % MODULUS
    print(f"sink {sink}")


main()
