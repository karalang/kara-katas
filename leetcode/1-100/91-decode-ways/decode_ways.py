# LeetCode #91: Decode Ways — Python mirror of decode_ways.kara.
#
# Bottom-up DP with a 2-cell rolling window. O(n) time, O(1) extra space.
# At position i: dp[i] = (one-digit ok ? dp[i-1] : 0) + (two-digit ok ? dp[i-2] : 0)
# with dp[0] = dp[1] = 1 once we've ruled out a leading '0'.

from __future__ import annotations


def decode_ways(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    if s[0] == '0':
        return 0

    # prev2 = dp[i-2], prev1 = dp[i-1]. Seeded for i = 1.
    prev2 = 1
    prev1 = 1

    for i in range(1, n):
        d1 = ord(s[i]) - ord('0')
        d0 = ord(s[i - 1]) - ord('0')
        two = d0 * 10 + d1

        cur = 0
        if 1 <= d1 <= 9:
            cur += prev1
        if 10 <= two <= 26:
            cur += prev2

        prev2 = prev1
        prev1 = cur

    return prev1


def report(s: str) -> None:
    print(f'decode_ways "{s}": {decode_ways(s)}')


def main() -> None:
    # The LeetCode reference cases.
    report("12")        # expect: 2
    report("226")       # expect: 3
    report("06")        # expect: 0

    # Mid-stream zero behaviour.
    report("10")        # expect: 1
    report("100")       # expect: 0
    report("101")       # expect: 1
    report("110")       # expect: 1
    report("301")       # expect: 0
    report("230")       # expect: 0
    report("27")        # expect: 1

    # Empty and single-digit.
    report("")          # expect: 0
    report("0")         # expect: 0
    report("1")         # expect: 1
    report("9")         # expect: 1

    # All twos and ones — Fibonacci-sequence count.
    report("11")        # expect: 2
    report("111")       # expect: 3
    report("1111")      # expect: 5
    report("11111")     # expect: 8
    report("111111")    # expect: 13

    # Long mixed cases.
    report("123123")    # expect: 9
    report("1234567")   # expect: 3
    report("2611055971756562")  # expect: 4


if __name__ == "__main__":
    main()
