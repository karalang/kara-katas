# LeetCode #1799: Maximize Score After N Operations -- the ★ arm in Python:
# dynamic programming over the set of numbers already taken, a bitmask.
from math import gcd


def max_score(nums):
    m = len(nums)
    full = 1 << m
    best = [0] * full
    for mask in range(full):
        taken = bin(mask).count("1")
        if taken % 2 == 1:
            continue
        op = taken // 2 + 1
        for i in range(m):
            if mask >> i & 1:
                continue
            for j in range(i + 1, m):
                if mask >> j & 1:
                    continue
                nxt = mask | 1 << i | 1 << j
                best[nxt] = max(best[nxt], best[mask] + op * gcd(nums[i], nums[j]))
    return best[full - 1]


seed = 1799


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{max_score([1, 2])} {max_score([3, 4, 6, 8])} {max_score([1, 2, 3, 4, 5, 6])}")
    print(f"{max_score([5, 5])} {max_score([2, 3])} {max_score([1, 1, 1, 1, 1, 1])} {max_score([6, 10, 15, 30])}")
    top = [1000000] * 14
    wide = [1 + next_random() % 1000000 for _ in range(14)]
    print(f"the most: {max_score(top)} {max_score(wide)}")
    check = 0
    for _ in range(1000):
        n = 2 * (1 + next_random() % 5)
        nums = [1 + next_random() % 60 for _ in range(n)]
        check = (check * 31 + max_score(nums)) % 1000000007
    print(f"1000 random cases: checksum {check}")


main()
