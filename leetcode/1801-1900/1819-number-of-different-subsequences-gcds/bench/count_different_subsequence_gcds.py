# LeetCode #1819: Number of Different Subsequences GCDs -- the bench in
# Python: the ★ arm over 100 calls on runs of 50000 to 99999 numbers cut
# from one list of 10^5 numbers from 1 to 2 * 10^5, built once, each run's
# length drawn from the checksum so far.
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


base = []
for _ in range(100000):
    base.append(1 + (next_random() * 32768 + next_random()) % 200000)
check = 0
for call in range(100):
    n = 50000 + (check + call) % 50000
    check = (check * 31 + count_different_subsequence_gcds(base[:n])) % 1000000007
print(f"100 calls: checksum {check}")
