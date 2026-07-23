"""Benchmark workload for LeetCode #85 — Maximal Rectangle (Python; scale lane)."""


def largest_rect(heights):
    n = len(heights)
    stack = []
    best = 0
    i = 0
    while i <= n:
        h = 0 if i == n else heights[i]
        while stack and heights[stack[-1]] >= h:
            top = stack[-1]
            height = heights[top]
            stack.pop()
            width = i if not stack else i - stack[-1] - 1
            area = height * width
            if area > best:
                best = area
        stack.append(i)
        i += 1
    return best


def maximal_rectangle(matrix, rows, cols):
    heights = [0] * cols
    best = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 1:
                heights[c] += 1
            else:
                heights[c] = 0
        a = largest_rect(heights)
        if a > best:
            best = a
    return best


def main():
    rows = 70
    cols = 70
    passes = 11000
    matrix = []
    state = 12345
    for _ in range(rows):
        rowv = []
        for _ in range(cols):
            state = (state * 1103515245 + 12345) & 2147483647
            rowv.append(1 if (state >> 16) % 100 < 62 else 0)
        matrix.append(rowv)

    sink = 0
    for p in range(passes):
        rr = p % rows
        cc = (p * 131 + 7) % cols
        matrix[rr][cc] = 1 - matrix[rr][cc]
        sink += maximal_rectangle(matrix, rows, cols)
    print(sink)


main()
