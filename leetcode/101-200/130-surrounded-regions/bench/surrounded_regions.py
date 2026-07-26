"""Benchmark harness for LeetCode #130 — Surrounded Regions.

Mirrors surrounded_regions.kara algorithm-for-algorithm, including the nested
list-of-lists board and the explicit position stack. Committed as the
correctness oracle; not a measured lane.
"""

ROWS = 300
COLS = 300
ITERS = 400


def flood(board, rows, cols, sr, sc):
    stack = [sr * cols + sc]
    while stack:
        pos = stack.pop()
        r = pos // cols
        c = pos % cols
        if board[r][c] == 1:
            board[r][c] = 2
            if r + 1 < rows:
                stack.append((r + 1) * cols + c)
            if r - 1 >= 0:
                stack.append((r - 1) * cols + c)
            if c + 1 < cols:
                stack.append(r * cols + (c + 1))
            if c - 1 >= 0:
                stack.append(r * cols + (c - 1))


def solve(board, rows, cols):
    for r in range(rows):
        for c in range(cols):
            on_border = r == 0 or r == rows - 1 or c == 0 or c == cols - 1
            if on_border and board[r][c] == 1:
                flood(board, rows, cols, r, c)
    for r in range(rows):
        for c in range(cols):
            board[r][c] = 1 if board[r][c] == 2 else 0


def main():
    pristine = []
    x = 5
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append((x // 65536) % 2)
        pristine.append(row)

    sink = 0
    for _ in range(ITERS):
        work = [list(row) for row in pristine]

        solve(work, ROWS, COLS)

        h = 0
        for p in range(ROWS):
            for q in range(COLS):
                h = (h * 31 + work[p][q]) % 1000000007
        sink = (sink + h) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
