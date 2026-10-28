# LeetCode #1005: Maximize Sum Of Array After K Negations -- counting
#
# Mirrors largest_sum.kara, the ★ arm, and its test harness; its output is
# byte-identical.


def largest_sum_after_k_negations(nums, k):
    count = [0] * 201
    for x in nums:
        count[x + 100] += 1
    left = k
    v = -100
    while v < 0 and left > 0:
        flip = min(count[v + 100], left)
        count[v + 100] -= flip
        count[100 - v] += flip
        left -= flip
        v += 1
    total = 0
    for v in range(-100, 101):
        total += v * count[v + 100]
    if left % 2 == 1:
        smallest = 0
        while count[smallest + 100] == 0:
            smallest += 1
        total -= 2 * smallest
    return total


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_nums(n, reach, neg, seed):
    nums = []
    for _ in range(n):
        size = next_random(seed) % (reach + 1)
        nums.append(-size if next_random(seed) % 8 < neg else size)
    return nums


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([4, 2, 3], 1),
        ([3, -1, 0, 2], 3),
        ([2, -3, -1, 5, -4], 2),
        ([-5], 1),
        ([-5], 2),
        ([5], 1),
        ([0], 3),
        ([-2, -3], 1),
        ([-8, 3, -5, -3, -4], 6),
        ([-1, -1, 1], 3),
        ([100, -100, 7], 4),
    ]
    for nums, k in examples:
        print(f"nums = {show(nums)}, k = {k} -> {largest_sum_after_k_negations(nums, k)}")
    n = 10000
    low = [-100] * n
    high = [100] * n
    turns = [-100 if i % 2 == 0 else 99 for i in range(n)]
    large = [
        ("10000 of -100, k = 10000", low, 10000),
        ("10000 of -100, k = 9999", low, 9999),
        ("10000 of 100, k = 9999", high, 9999),
        ("10000 of 100, k = 10000", high, 10000),
        ("-100, 99 in turn, k = 5001", turns, 5001),
        ("-100, 99 in turn, k = 2500", turns, 2500),
    ]
    for name, nums, k in large:
        print(f"{name} -> {largest_sum_after_k_negations(nums, k)}")
    seed = [1005]
    for count, most, reach in [(3000, 8, 6), (1000, 100, 100), (100, 2000, 100), (3, 10000, 100)]:
        total = 0
        acc = 0
        check = 0
        for _ in range(count):
            size = 1 + next_random(seed) % most
            neg = next_random(seed) % 9
            nums = random_nums(size, reach, neg, seed)
            k = 1 + next_random(seed) % min(2 * size + 1, 10000)
            got = largest_sum_after_k_negations(nums, k)
            total += size
            acc += got
            check = (check * 31 + got % 1000000007 + 1000000007) % 1000000007
        print(f"{count} random arrays of {total} numbers: answers sum to {acc}, checksum {check}")


main()
