# LeetCode #1819: Number of Different Subsequences GCDs -- the ★ arm in Python
import sys

sys.setrecursionlimit(10000)


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def count_different_subsequence_gcds(nums):
    top = max(nums)
    present = [False] * (top + 1)
    for x in nums:
        present[x] = True
    count = 0
    for g in range(1, top + 1):
        d = 0
        m = g
        while m <= top and d != g:
            if present[m]:
                d = gcd(d, m)
            m += g
        if d == g:
            count += 1
    return count


seed = 1819


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


f = count_different_subsequence_gcds
print(f([6, 10, 3]), f([5, 15, 40, 5, 6]))
print(f([1]), f([7, 7, 7]), f([4, 8, 16]), f([9, 10]), f([200000]))
n = 100000
print(f"the most: {f(list(range(1, n + 1)))} {f([2 * x for x in range(1, n + 1)])}")
check = 0
for _ in range(3000):
    ln = 1 + next_random() % 8
    nums = [1 + next_random() % 60 for _ in range(ln)]
    check = (check * 31 + f(nums)) % 1000000007
print(f"3000 random cases: checksum {check}")
