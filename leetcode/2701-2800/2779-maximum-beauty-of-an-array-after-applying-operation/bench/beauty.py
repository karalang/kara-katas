# LeetCode #2779: Maximum Beauty of an Array After Applying Operation --
# the bench in Python: the ★ arm over 20 arrays of 10^5 numbers, all
# drawn first, then each answered 10 times, every answer sorting its own
# copy.


def maximum_beauty(nums, k):
    s = sorted(nums)
    best = 0
    lo = 0
    for hi in range(len(s)):
        while s[hi] - s[lo] > 2 * k:
            lo += 1
        best = max(best, hi - lo + 1)
    return best


seed = 2779


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 20
    rounds = 10
    cases = []
    for _ in range(count):
        nums = [wide() % 100001 for _ in range(100000)]
        cases.append((nums, wide() % 1001))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            b = maximum_beauty(nums, k)
            total += b
            check = (check * 31 + b + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: beauties sum to {total}, checksum {check}")


main()
