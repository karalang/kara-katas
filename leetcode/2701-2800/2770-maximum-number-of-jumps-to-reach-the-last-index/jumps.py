# LeetCode #2770: Maximum Number of Jumps to Reach the Last Index -- the
# ★ arm in Python (jumps.kara): the most jumps that reach each index from
# 0, each index taking the best of the reached indices before it within
# target of its number, plus one.


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


def fold(a, acc):
    if a >= 0:
        acc[0] += 1
        acc[1] += a
    acc[2] = (acc[2] * 31 + a + 1) % 1000000007


def main():
    for target in [2, 3, 0]:
        print(maximum_jumps([1, 3, 6, 4, 1, 2], target))
    print(maximum_jumps(list(range(1000)), 1))
    print(maximum_jumps([-1000000000 if i % 2 == 0 else 1000000000 for i in range(1000)], 2000000000))
    equal = [7] * 1000
    print(maximum_jumps(equal, 0))
    equal[999] = 8
    print(maximum_jumps(equal, 0))
    acc = [0, 0, 0]
    for _ in range(3000):
        n = next_random() % 11 + 2
        nums = [next_random() % 10 for _ in range(n)]
        target = next_random() % 5
        fold(maximum_jumps(nums, target), acc)
    print(f"3000 small arrays: {acc[0]} reached, jumps sum to {acc[1]}, checksum {acc[2]}")
    acc = [0, 0, 0]
    for _ in range(20):
        nums = [wide() % 2000000001 - 1000000000 for _ in range(1000)]
        target = wide() % 2000000001
        fold(maximum_jumps(nums, target), acc)
    print(f"20 arrays of 1000: {acc[0]} reached, jumps sum to {acc[1]}, checksum {acc[2]}")


main()
