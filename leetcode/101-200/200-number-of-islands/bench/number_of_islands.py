"""Benchmark workload for LeetCode #200 — Number of Islands (Python; scale lane)."""

import sys


def num_islands(grid, rows, cols):
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r * cols + c] == 1:
                count += 1
                stack = [r * cols + c]
                grid[r * cols + c] = 0
                while len(stack) > 0:
                    idx = stack.pop()
                    cr = idx // cols
                    cc = idx % cols
                    if cr > 0 and grid[(cr - 1) * cols + cc] == 1:
                        grid[(cr - 1) * cols + cc] = 0
                        stack.append((cr - 1) * cols + cc)
                    if cr + 1 < rows and grid[(cr + 1) * cols + cc] == 1:
                        grid[(cr + 1) * cols + cc] = 0
                        stack.append((cr + 1) * cols + cc)
                    if cc > 0 and grid[cr * cols + (cc - 1)] == 1:
                        grid[cr * cols + (cc - 1)] = 0
                        stack.append(cr * cols + (cc - 1))
                    if cc + 1 < cols and grid[cr * cols + (cc + 1)] == 1:
                        grid[cr * cols + (cc + 1)] = 0
                        stack.append(cr * cols + (cc + 1))
    return count


def main():
    rows = 80
    cols = 80
    passes = 13000
    total = rows * cols

    master = [0] * total
    state = 12345
    for g in range(total):
        state = (state * 1103515245 + 12345) & 2147483647
        master[g] = 1 if (state >> 16) % 100 < 45 else 0

    work = [0] * total
    sink = 0
    for _ in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % total
        master[idx] = 1 - master[idx]
        for i in range(total):
            work[i] = master[i]
        sink += num_islands(work, rows, cols)
    print(sink)


main()
