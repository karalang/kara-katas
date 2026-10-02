"""LeetCode #329: Longest Increasing Path in a Matrix — Python mirror.

Mirrors longest_increasing_path.kara: a depth-first search from every cell
that remembers each cell's answer. Prints the same lines.
"""
import sys

sys.setrecursionlimit(100000)


def longest_from(matrix, memo, r, c):
    if memo[r][c] > 0:
        return memo[r][c]
    rows, cols = len(matrix), len(matrix[0])
    here = matrix[r][c]
    best = 1
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > here:
            best = max(best, 1 + longest_from(matrix, memo, nr, nc))
    memo[r][c] = best
    return best


def longest_increasing_path(matrix):
    if not matrix or not matrix[0]:
        return 0
    memo = [[0] * len(row) for row in matrix]
    best = 0
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            best = max(best, longest_from(matrix, memo, r, c))
    return best


seed = 329


def next_rand():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_matrix(rows, cols, rng):
    return [[next_rand() % rng for _ in range(cols)] for _ in range(rows)]


def report(matrix):
    print(f"{matrix} -> {longest_increasing_path(matrix)}")


def main():
    report([[9, 9, 4], [6, 6, 8], [2, 1, 1]])
    report([[3, 4, 5], [3, 2, 6], [2, 2, 1]])
    report([[1]])

    report([[1, 2, 3, 4, 5]])
    report([[5], [4], [3], [2], [1]])
    report([[7, 7], [7, 7]])
    report([[1, 2, 3], [6, 5, 4], [7, 8, 9]])
    report([[-9223372036854775808, 9223372036854775807]])

    n = 100
    snake = [[r * n + c if r % 2 == 0 else r * n + (n - 1 - c) for c in range(n)] for r in range(n)]
    print(f"snake {n}x{n} -> {longest_increasing_path(snake)}")

    for _ in range(3):
        rows = next_rand() % 4 + 1
        cols = next_rand() % 4 + 1
        report(random_matrix(rows, cols, 10))
    for rows, cols, rng in [(50, 50, 10), (50, 50, 1000), (200, 300, 100000), (300, 200, 5)]:
        m = random_matrix(rows, cols, rng)
        print(f"{rows}x{cols} in [0, {rng}) -> {longest_increasing_path(m)}")


import threading

threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
