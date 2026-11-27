# LeetCode #1838: Frequency of the Most Frequent Element -- the bench in Python: the ★ arm over
# 200 calls on the first 50000 to 99999 of one list of 10^5 numbers from 1
# to 10^5, built once, with `k` from 1 to 10^5, each run's length and `k`
# drawn from the checksum so far. Each call copies its run, and the arm
# sorts a copy of its own.


def max_frequency(nums, k):
    s = sorted(nums)
    best = 0
    first = 0
    total = 0
    for last in range(len(s)):
        total += s[last]
        while s[last] * (last - first + 1) - total > k:
            total -= s[first]
            first += 1
        best = max(best, last - first + 1)
    return best


def main():
    seed = 1838

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    base = []
    for _ in range(100000):
        hi = next_random()
        base.append(1 + (hi * 32768 + next_random()) % 100000)
    check = 0
    for call in range(200):
        n = 50000 + (check + call) % 50000
        k = 1 + (check * 7 + call) % 100000
        run = base[:n]
        check = (check * 31 + max_frequency(run, k)) % 1000000007
    print(f"200 calls: checksum {check}")


main()
