# LeetCode #1004: Max Consecutive Ones III -- a sliding window
#
# Mirrors longest_ones.kara, the ★ arm, and its test harness; its output is
# byte-identical.


def longest_ones(nums, k):
    left = 0
    zeros = 0
    best = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_bits(n, ones, seed):
    return [1 if next_random(seed) % 8 < ones else 0 for _ in range(n)]


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2),
        ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3),
        ([1, 1, 1, 1], 0),
        ([0, 0, 0], 0),
        ([0, 0, 0], 3),
        ([0], 0),
        ([0], 1),
        ([1, 0, 1], 0),
        ([1, 0, 1], 1),
        ([1, 1, 0, 1, 1, 0, 0, 1], 1),
    ]
    for nums, k in examples:
        print(f"nums = {show(nums)}, k = {k} -> {longest_ones(nums, k)}")
    n = 100000
    large = [
        ("100000 ones, k = 0", [1] * n, 0),
        ("100000 zeros, k = 0", [0] * n, 0),
        ("100000 zeros, k = 100000", [0] * n, 100000),
        ("1, 0 in turn, k = 25000", [1 - i % 2 for i in range(n)], 25000),
    ]
    for name, nums, k in large:
        print(f"{name} -> {longest_ones(nums, k)}")
    seed = [1004]
    for count, most in [(3000, 12), (1000, 100), (100, 2000), (3, 100000)]:
        total = 0
        total_sum = 0
        check = 0
        for _ in range(count):
            size = 1 + next_random(seed) % most
            density = next_random(seed) % 9
            nums = random_bits(size, density, seed)
            k = next_random(seed) % (size + 1) // (1 + next_random(seed) % 8)
            got = longest_ones(nums, k)
            total += size
            total_sum += got
            check = (check * 31 + got + 1) % 1000000007
        print(f"{count} random arrays of {total} numbers: answers sum to {total_sum}, checksum {check}")


main()
