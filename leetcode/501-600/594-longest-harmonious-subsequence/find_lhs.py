# LeetCode #594: Longest Harmonious Subsequence -- count, then pair.
#
# Mirrors find_lhs.kara: count each value in a dict; for every value v
# with v + 1 also present, count[v] + count[v + 1] is a candidate.


def find_lhs(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    best = 0
    for v, c in count.items():
        d = count.get(v + 1)
        if d is not None:
            best = max(best, c + d)
    return best


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(nums):
    print(f"{nums} -> {find_lhs(nums)}")


def main():
    show([1, 3, 2, 2, 5, 2, 3, 7])
    show([1, 2, 3, 4])
    show([1, 1, 1, 1])
    show([7])
    show([4, 5])
    show([4, 6, 4, 6])
    show([1000000000, 999999999, 1000000000, -1000000000, -999999999])
    show([-3, -2, -2, -1, -3, -3])
    show([9, 9, 9, 9, 1, 2, 3, 4])
    show([1, 2, 5, 6, 6, 5, 6])
    seed = [594]
    few = []
    apart = []
    for k in range(20000):
        few.append(step(seed) % 50)
        apart.append(2 * k - 20000)
    print(f"20000 values from 0 to 49 -> {find_lhs(few)}")
    print(f"20000 values two apart -> {find_lhs(apart)}")
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step(seed) % 40
        rng = 1 + step(seed) % 12
        low = step(seed) % 21 - 10
        nums = [low + step(seed) % rng for _ in range(n)]
        got = find_lhs(nums)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random arrays: total {total}, checksum {checksum}")


main()
