# LeetCode #2770: Maximum Number of Jumps to Reach the Last Index -- the
# bench in Python: the ★ arm over 40 arrays of 1000 numbers, all drawn
# first, then each answered 5 times.


def maximum_jumps(nums, target):
    n = len(nums)
    most = [-1] * n
    most[0] = 0
    for j in range(1, n):
        for i in range(j):
            if most[i] >= 0 and abs(nums[j] - nums[i]) <= target:
                most[j] = max(most[j], most[i] + 1)
    return most[n - 1]


seed = 2770


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    b = next_random()
    return (a * 32768 + b) * 32768 + next_random()


def main():
    count = 40
    rounds = 5
    cases = []
    for _ in range(count):
        nums = [wide() % 2000000001 - 1000000000 for _ in range(1000)]
        cases.append((nums, wide() % 2000000001))
    reached = total = check = 0
    for r in range(rounds):
        for nums, target in cases:
            a = maximum_jumps(nums, target)
            if a >= 0:
                reached += 1
                total += a
            check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} arrays of 1000, {rounds} rounds: {reached} reached, jumps sum to {total}, checksum {check}")


main()
