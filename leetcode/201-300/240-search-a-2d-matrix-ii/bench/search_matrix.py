"""Benchmark harness for LeetCode #240 — Search a 2D Matrix II.

Mirrors search_matrix.kara algorithm-for-algorithm. Committed as the
correctness oracle; not a measured lane.
"""

ROWS = 1000
COLS = 1000
ITERS = 120000


def search_matrix(flat, rows, cols, target):
    if rows == 0 or cols == 0:
        return False
    r = 0
    c = cols - 1
    while r < rows and c >= 0:
        v = flat[r * cols + c]
        if v == target:
            return True
        elif v > target:
            c -= 1
        else:
            r += 1
    return False


def main():
    flat = []
    for r in range(ROWS):
        for c in range(COLS):
            flat.append(r * 3 + c * 5)
    maxv = (ROWS - 1) * 3 + (COLS - 1) * 5

    sink = 0
    x = 12345
    for it in range(ITERS):
        x = (x * 1103515245 + 12345) % 2147483648
        target = (x // 65536) % (maxv + 2)
        if search_matrix(flat, ROWS, COLS, target):
            sink = (sink + it + 1) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
