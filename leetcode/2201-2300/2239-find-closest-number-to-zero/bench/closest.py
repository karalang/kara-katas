# LeetCode #2239: Find Closest Number to Zero -- the benchmark's Python
# mirror of closest.kara: one scan, a number kept when nearer to zero,
# or as near and larger.


def find_closest_number(nums):
    closest = nums[0]
    for x in nums:
        if abs(x) < abs(closest) or (abs(x) == abs(closest) and x > closest):
            closest = x
    return closest


seed = 2239


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    nums = [wide_random() % 200001 - 100000 for _ in range(1000)]
    check = 0
    for _ in range(100000):
        # punch: one number drawn again before each pass
        at = next_random() % 1000
        nums[at] = wide_random() % 200001 - 100000
        check = (check * 31 + find_closest_number(nums) + 100000) % 1000000007
    print(f"100000 passes over 1000 numbers: checksum {check}")


main()
