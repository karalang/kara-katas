"""LeetCode 85 — Maximal Rectangle (Python mirror / oracle).

Row-by-row histogram of consecutive-1 heights, then largest-rectangle-in-
histogram via a monotonic stack. O(R*C). Mirrors the Kāra version.
"""


def largest_rect(heights):
    n = len(heights)
    stack = []
    best = 0
    for i in range(n + 1):
        h = 0 if i == n else heights[i]
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            height = heights[top]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best


def maximal_rectangle(matrix):
    if not matrix:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for r_ in matrix:
        for c in range(cols):
            heights[c] = heights[c] + 1 if r_[c] == 1 else 0
        best = max(best, largest_rect(heights))
    return best


def run(matrix):
    print(maximal_rectangle(matrix))


def main():
    run([[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]])
    run([[0]])
    run([[1]])
    run([[1, 1], [1, 1]])


main()
