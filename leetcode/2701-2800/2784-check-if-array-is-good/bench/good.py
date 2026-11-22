# LeetCode #2784: Check if Array is Good -- the bench in Python: the ★
# arm over 50000 arrays of 100 numbers, base[99] shuffled and two in
# three with one number changed to one up to 200, all drawn first, then
# each answered 40 times.


def is_good(nums):
    n = len(nums) - 1
    if n < 1:
        return False
    counts = [0] * (n + 1)
    for v in nums:
        if v < 1 or v > n:
            return False
        counts[v] += 1
    return all(counts[v] == 1 for v in range(1, n)) and counts[n] == 2


seed = 2784


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled_base(n):
    nums = list(range(1, n + 1)) + [n]
    for i in range(n, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    count = 50000
    rounds = 40
    cases = []
    for _ in range(count):
        nums = shuffled_base(99)
        if next_random() % 3 != 0:
            at = next_random() % 100
            nums[at] = next_random() % 200 + 1
        cases.append(nums)
    good = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            g = is_good(nums)
            if g:
                good += 1
            check = (check * 31 + (2 if g else 1) + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: {good} good, checksum {check}")


main()
