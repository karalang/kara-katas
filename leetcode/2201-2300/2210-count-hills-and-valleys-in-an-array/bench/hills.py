# benchmark's Python mirror of hills.kara (LeetCode #2210, the ★ arm): one
# pass keeping the last number that differs from the current one, a run
# counted once, at its end.


def count_hill_valley(nums):
    count = 0
    left = nums[0]
    for i in range(1, len(nums) - 1):
        if nums[i] == nums[i + 1]:
            continue
        right = nums[i + 1]
        if (nums[i] > left and nums[i] > right) or (nums[i] < left and nums[i] < right):
            count += 1
        if nums[i] != left:
            left = nums[i]
    return count


seed = 2210


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(2000):
        top = [3, 10, 100][a % 3]
        arrays.append([next_random() % top + 1 for _ in range(100)])
    # every array counted once per pass
    check = 0
    for p in range(100):
        for nums in arrays:
            check = (check * 31 + count_hill_valley(nums) + p) % 1000000007
    print(f"100 passes over 2000 arrays: checksum {check}")


main()
