# LeetCode #2740: Find the Value of the Partition -- the bench
# (partition.kara in Python): sort a copy, and the least gap between
# neighbours.


def find_value_of_partition(nums):
    nums = sorted(nums)
    best = nums[1] - nums[0]
    for i in range(2, len(nums)):
        best = min(best, nums[i] - nums[i - 1])
    return best


def main():
    count, n, rounds = 20, 100000, 10
    seed = 2740
    arrays = []
    for _ in range(count):
        nums = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            hi = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            lo = seed // 65536
            nums.append((hi * 32768 + lo) % 1000000000 + 1)
        arrays.append(nums)
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            value = find_value_of_partition(nums)
            total += value
            check = (check * 31 + value + r) % 1000000007
    print(f"{count} arrays of {n} numbers, {rounds} rounds: values sum to {total}, checksum {check}")


main()
