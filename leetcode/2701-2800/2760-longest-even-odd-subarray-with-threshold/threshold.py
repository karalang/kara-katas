# LeetCode #2760: Longest Even Odd Subarray With Threshold -- the ★ arm in
# Python (threshold.kara): one pass with the length of the good run
# ending at each number.


def longest_alternating_subarray(nums, threshold):
    best = run = 0
    for i, x in enumerate(nums):
        if x > threshold:
            run = 0
        elif run > 0 and x % 2 != nums[i - 1] % 2:
            run += 1
        elif x % 2 == 0:
            run = 1
        else:
            run = 0
        best = max(best, run)
    return best


seed = 2760


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(longest_alternating_subarray([3, 2, 5, 4], 5))
    print(longest_alternating_subarray([1, 2], 2))
    print(longest_alternating_subarray([2, 3, 4, 5], 4))
    print(longest_alternating_subarray([1, 3, 5], 100))
    print(longest_alternating_subarray([2 + i % 2 for i in range(100)], 3))
    print(longest_alternating_subarray([2, 3, 4, 50, 6, 7], 10))
    total = check = 0
    for _ in range(20000):
        n = next_random() % 100 + 1
        top = next_random() % 100 + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        threshold = next_random() % 100 + 1
        length = longest_alternating_subarray(nums, threshold)
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"20000 arrays: lengths sum to {total}, checksum {check}")


main()
