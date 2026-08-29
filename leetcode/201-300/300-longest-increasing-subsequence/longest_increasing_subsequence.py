"""LeetCode 300 - Longest Increasing Subsequence.

Mirror of longest_increasing_subsequence.kara: same patience-sorting algorithm,
same hand-written binary search, same output. Deliberately not using bisect so
the comparison is algorithm-for-algorithm - bisect_left would hand the inner
loop to C and measure something different.
"""


def lis_length(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0

    tails: list[int] = []

    for i in range(n):
        x = nums[i]

        # Leftmost index with tails[idx] >= x.
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid

        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x

    return len(tails)


def report(nums: list[int]) -> None:
    body = ", ".join(str(v) for v in nums)
    print(f"[{body}] -> {lis_length(nums)}")


def main() -> None:
    report([10, 9, 2, 5, 3, 7, 101, 18])
    report([0, 1, 0, 3, 2, 3])
    report([7, 7, 7, 7])
    report([])
    report([1])
    report([5, 4, 3, 2, 1])
    report([1, 2, 3, 4, 5])
    report([2, 2, 2, 1, 3])
    report([-5, -3, -8, 0, -1])
    report([1, 3, 2, 4, 3, 5])


if __name__ == "__main__":
    main()
