# LeetCode #2789: Largest Element in an Array after Merge Operations --
# the bench in Python: the ★ arm over 20 arrays of 10^5 numbers up to
# 10^6, all drawn first, then each answered 100 times.


def max_array_value(nums):
    n = len(nums)
    held = nums[n - 1]
    for i in range(n - 2, -1, -1):
        held = held + nums[i] if nums[i] <= held else nums[i]
    return held


seed = 2789


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 20
    rounds = 100
    cases = []
    for _ in range(count):
        cases.append([wide() % 1000000 + 1 for _ in range(100000)])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            a = max_array_value(nums)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: largest sum to {total}, checksum {check}")


main()
