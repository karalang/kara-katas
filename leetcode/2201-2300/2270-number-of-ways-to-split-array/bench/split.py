# LeetCode #2270: Number of Ways to Split Array -- the bench, the ★ arm.


def ways_to_split_array(nums):
    total = sum(nums)
    left = 0
    ways = 0
    for i in range(len(nums) - 1):
        left += nums[i]
        if left >= total - left:
            ways += 1
    return ways


# ---- bench harness ---------------------------------------------------------

seed = 2270


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(100):
        nums = [next_random() % 200001 - 100000 for _ in range(100000)]
        check = (check * 31 + ways_to_split_array(nums)) % 1000000007
    print(f"100 arrays of 10^5: checksum {check}")


main()
