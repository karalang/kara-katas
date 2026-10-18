# LeetCode #704 bench: the ★ arm in Python. See the .kara twin for the
# workload.

seed = 704


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def main():
    arrays = []
    for _ in range(100):
        nums = []
        v = -9999
        for _ in range(10000):
            nums.append(v)
            v += 1 + next_random() % 2
        arrays.append(nums)
    found = 0
    checksum = 0
    for _ in range(5):
        for nums in arrays:
            for target in range(-9999, 10000):
                at = search(nums, target)
                if at >= 0:
                    found += 1
                checksum = (checksum * 31 + at + 1) % 1000000007
    print(f"5 rounds of 100 arrays of 10000: {found} found, checksum {checksum}")


main()
