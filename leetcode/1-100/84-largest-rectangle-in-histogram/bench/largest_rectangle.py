"""Benchmark workload — Largest Rectangle in Histogram (LeetCode #84).

Python mirror of bench/largest_rectangle.kara. Each iteration builds a fresh sawtooth
histogram (heights[j] = (j + iter) % 50, N=2000), runs the monotonic-stack
largest_rectangle, and adds the area into an associative sum. Runs a smaller K
(pure-Python is slow); timed separately, NOT cross-checked. See ../README.md.
"""


def largest_rectangle(heights, n):
    stack = []
    max_area = 0
    i = 0
    while i <= n:
        h = heights[i] if i < n else 0
        while len(stack) > 0 and heights[stack[-1]] > h:
            top = stack.pop()
            height = heights[top]
            width = i if len(stack) == 0 else i - stack[-1] - 1
            area = height * width
            if area > max_area:
                max_area = area
        stack.append(i)
        i += 1
    return max_area


def build(n, iter_):
    return [(j + iter_) % 50 for j in range(n)]


def main():
    n = 2000
    total = 4000
    total_sum = 0
    for k in range(total):
        h = build(n, k)
        total_sum += largest_rectangle(h, n)
    print(total_sum)


if __name__ == "__main__":
    main()
