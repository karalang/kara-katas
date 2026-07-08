"""LeetCode #69: Sqrt(x) — integer square root by binary search, O(log x).

Mirror of sqrtx.kara: the answer is the largest r with r*r <= x, found by binary
search on the monotone predicate. Same twenty-seven cases and the same output
shape (one `sqrt(x) = r` per line, then a `sums:` fold) so the files diff
line-for-line. (The Newton and bit-by-bit variants live only in Kāra; this mirror
tracks the ★.)
"""

from __future__ import annotations


def my_sqrt(x: int) -> int:
    lo, hi, ans = 0, x, 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if mid * mid <= x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def report(x: int, acc: list[str]) -> None:
    r = my_sqrt(x)
    print(f"sqrt({x}) = {r}")
    acc.append(str(r))


def main() -> None:
    acc: list[str] = []
    for x in [0, 1, 2, 3, 4, 5, 8, 9, 10, 15, 16, 17, 24, 25, 26, 35, 36, 48, 49,
              99, 100, 101, 2147395600, 2147483647, 1000000000, 46340, 46341]:
        report(x, acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
