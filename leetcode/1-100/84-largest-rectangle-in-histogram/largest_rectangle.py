"""LeetCode #84: Largest Rectangle in Histogram — monotonic stack, O(n).

Mirror of largest_rectangle.kara. Keep a stack of bar indices with strictly increasing
heights; when the current bar is shorter than the stack top, pop it and settle its
largest rectangle (height = heights[top], width spans from just past the new top to
just before the current bar). A virtual height-0 sentinel at index n flushes the rest.
Same ten cases and output shape (an area per case, then a `sink:` fold) so the files
diff line-for-line.
"""

from __future__ import annotations


def largest_rectangle(heights: list[int], n: int) -> int:
    stack: list[int] = []
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


def report(heights: list[int], n: int, acc: list[int]) -> None:
    area = largest_rectangle(heights, n)
    print(area)
    acc[0] = (acc[0] * 131 + (area + 1)) % 1000000007


def main() -> None:
    acc = [0]
    report([2, 1, 5, 6, 2, 3], 6, acc)
    report([2, 4], 2, acc)
    report([], 0, acc)
    report([5], 1, acc)
    report([1, 1, 1, 1], 4, acc)
    report([6, 2, 5, 4, 5, 1, 6], 7, acc)
    report([0, 0, 0], 3, acc)
    report([4, 2, 0, 3, 2, 5], 6, acc)
    report([1, 2, 3, 4, 5], 5, acc)
    report([5, 4, 3, 2, 1], 5, acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
