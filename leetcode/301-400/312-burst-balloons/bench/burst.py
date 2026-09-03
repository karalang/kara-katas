"""Benchmark workload for LeetCode #312 - Burst Balloons.

Mirror of burst.kara: same interval DP, same flat table reused across passes,
same serial dependency between passes, same masked sink. Kept
algorithm-for-algorithm so the cross-language comparison is honest.
"""


def solve(a, w, dp):
    for length in range(2, w):
        for i in range(0, w - length):
            j = i + length
            ai = a[i]
            aj = a[j]
            base = i * w
            best = 0
            for k in range(i + 1, j):
                coins = dp[base + k] + dp[k * w + j] + ai * a[k] * aj
                if coins > best:
                    best = coins
            dp[base + j] = best
    return dp[w - 1]


def main():
    n = 300
    w = n + 2
    passes = 88

    a = [1]
    state = 987654321
    for _ in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        a.append(1 + state % 50)
    a.append(1)

    dp = [0] * (w * w)

    checksum = 0
    for _ in range(passes):
        idx = 1 + checksum % n
        a[idx] = 1 + (a[idx] + checksum) % 50
        total = solve(a, w, dp)
        checksum = (checksum + total) & 1073741823

    print("checksum " + str(checksum))


if __name__ == "__main__":
    main()
