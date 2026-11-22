# LeetCode #2817: Minimum Absolute Difference Between Elements With
# Constraint -- the bench in Python: the ★ arm over 10 arrays of 10^5
# distinct numbers up to 10^9, shuffled, x from 0 to 10^5 - 1, all drawn
# first, then each answered 3 times. Python has no sorted set, so the
# window is a list kept in order by `bisect.insort`, each insert moving
# the larger numbers up one place.
import bisect


def min_absolute_difference(nums, x):
    behind = []
    best = 1 << 62
    for i in range(x, len(nums)):
        bisect.insort(behind, nums[i - x])
        v = nums[i]
        k = bisect.bisect_left(behind, v)
        if k < len(behind):
            best = min(best, behind[k] - v)
        if k > 0:
            best = min(best, v - behind[k - 1])
        if best == 0:
            break
    return best


seed = 2817


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 10, 3, 100000
    cases = []
    for _ in range(count):
        nums = [i * 10000 + wide() % 10000 + 1 for i in range(n)]
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        cases.append((nums, wide() % n))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, x in cases:
            a = min_absolute_difference(nums, x)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: differences sum to {total}, checksum {check}")


main()
