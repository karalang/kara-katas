"""LeetCode #70: Climbing Stairs — two rolling counters, O(n) time, O(1) space.

Mirror of climbing_stairs.kara: ways(n) = ways(n-1) + ways(n-2) with ways(1)=1,
ways(2)=2 (the Fibonacci recurrence), carried in two scalars rolled forward.
Same eleven cases and the same output shape (one `climb(n) = ways` per line, then
a `sums:` fold) so the files diff line-for-line. (The full-DP and matrix-power
variants live only in Kāra; this mirror tracks the ★.)
"""

from __future__ import annotations


def climb(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2  # ways(1), ways(2)
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def report(n: int, acc: list[str]) -> None:
    ways = climb(n)
    print(f"climb({n}) = {ways}")
    acc.append(str(ways))


def main() -> None:
    acc: list[str] = []
    for n in [1, 2, 3, 4, 5, 6, 10, 15, 20, 30, 45]:
        report(n, acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
