# LeetCode #2765: Longest Alternating Subarray -- the ★ arm in Python
# (alternating.kara): one pass with the length of the alternating run
# ending here; a run grows when the number equals the one two back, and
# otherwise a step up of 1 starts a run of 2.


def alternating_subarray(nums):
    best = -1
    run = 1
    for i in range(1, len(nums)):
        if run >= 2 and nums[i] == nums[i - 2]:
            run += 1
        elif nums[i] - nums[i - 1] == 1:
            run = 2
        else:
            run = 1
        if run >= 2:
            best = max(best, run)
    return best


seed = 2765


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(alternating_subarray([2, 3, 4, 3, 4]))
    print(alternating_subarray([4, 5, 6]))
    print(alternating_subarray([5, 5, 5]))
    print(alternating_subarray([3, 2, 3, 2]))
    print(alternating_subarray([7 + i % 2 for i in range(100)]))
    print(alternating_subarray([1, 2, 1, 2, 3, 2, 3, 2, 3]))
    total = 0
    check = 0
    for _ in range(20000):
        n = next_random() % 99 + 2
        top = next_random() % 4 + 2
        nums = [next_random() % top + 1 for _ in range(n)]
        a = alternating_subarray(nums)
        total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"20000 arrays: lengths sum to {total}, checksum {check}")


main()
