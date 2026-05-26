# LeetCode #11: Container With Most Water — Python mirror of container.kara.
#
# Same two-pointer O(n) algorithm. `min` is inlined as a conditional so the
# control-flow shape matches the Kara version line-for-line.


def max_area(heights: list[int]) -> int:
    n = len(heights)
    if n < 2:
        return 0
    lo = 0
    hi = n - 1
    best = 0
    while lo < hi:
        h_lo = heights[lo]
        h_hi = heights[hi]
        h = h_lo if h_lo < h_hi else h_hi
        area = h * (hi - lo)
        if area > best:
            best = area
        # Advance the shorter side. Ties go either direction; we advance lo.
        if h_lo < h_hi:
            lo += 1
        else:
            hi -= 1
    return best


def report(heights: list[int]) -> None:
    print(max_area(heights))


def main() -> None:
    report([1, 8, 6, 2, 5, 4, 8, 3, 7])
    report([1, 1])
    report([4, 3, 2, 1, 4])
    report([1, 2, 3, 4, 5])
    report([5, 4, 3, 2, 1])
    report([3, 3, 3, 3])
    report([2, 3, 4, 5, 18, 17, 6])
    report([2, 0, 3])
    report([2, 3])
    report([5])
    report([1, 2, 4, 3, 5, 9, 1, 2, 7, 6, 8, 4, 3, 2])


if __name__ == "__main__":
    main()
