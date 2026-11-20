# LeetCode #1248 bench, in Python: the ★ arm (prefix counts of odd values
# in a list indexed by count) on 50 random arrays of 50000 values built
# once, each with its own chance of an odd value, each asked with 10
# random k; every answer folded into a checksum.


def number_of_subarrays(nums, k):
    prefixes = [0] * (len(nums) + 1)
    prefixes[0] = 1
    odd = 0
    nice = 0
    for v in nums:
        odd += v % 2
        if odd >= k:
            nice += prefixes[odd - k]
        prefixes[odd] += 1
    return nice


seed = 1248


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(50):
        percent = next_random() % 101
        nums = []
        for _ in range(50000):
            v = next_random() % 50000 + 1
            nums.append(2 * v - 1 if next_random() % 100 < percent else 2 * v)
        arrays.append(nums)
    check = 0
    for nums in arrays:
        odd = sum(1 for v in nums if v % 2 == 1)
        for _ in range(100):
            k = next_random() % (odd + 1) + 1
            check = (check * 131 + number_of_subarrays(nums, k)) % 1000000007
    print(f"50 arrays of 50000 values, 100 k each: checksum {check}")


main()
