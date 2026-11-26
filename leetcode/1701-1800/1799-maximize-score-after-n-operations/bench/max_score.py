# LeetCode #1799: Maximize Score After N Operations -- the bench in Python:
# the ★ arm over 100 random lists of 14 numbers built once, 100 calls.
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
    lists = [[1 + next_random() % 1000000 for _ in range(14)] for _ in range(100)]
    check = 0
    for call in range(100):
        nums = lists[(check + call) % 100]
        check = (check * 31 + max_score(nums)) % 1000000007
    print(f"100 calls over 100 lists of 14 numbers: checksum {check}")


main()
