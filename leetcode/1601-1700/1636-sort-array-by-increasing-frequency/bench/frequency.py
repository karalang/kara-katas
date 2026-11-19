# LeetCode #1636: Sort Array by Increasing Frequency -- the bench's Python
# mirror: the ★ arm on 50000 random arrays of 100 values from -100 to 100,
# all drawn first.

from collections import Counter


def frequency_sort(nums):
    count = Counter(nums)
    return sorted(nums, key=lambda x: (count[x], -x))


seed = 1636


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[next_random() % 201 - 100 for _ in range(100)] for _ in range(50000)]
    check = 0
    for nums in arrays:
        for x in frequency_sort(nums):
            check = (check * 31 + x + 1000) % 1000000007
    print(f"50000 arrays of 100 values: checksum {check}")


main()
