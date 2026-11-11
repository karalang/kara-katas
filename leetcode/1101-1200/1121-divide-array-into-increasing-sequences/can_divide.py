# LeetCode #1121: Divide Array Into Increasing Sequences -- Python mirror
# of the ★ arm.

seed = 1121


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def can_divide_into_subsequences(nums, k):
    longest = run = 0
    for i in range(len(nums)):
        run = run + 1 if i > 0 and nums[i] == nums[i - 1] else 1
        longest = max(longest, run)
    return longest * k <= len(nums)


def random_sorted(n, top):
    return sorted(next_random() % top + 1 for _ in range(n))


def main():
    cases = [([1, 2, 2, 3, 3, 4, 4], 3), ([5, 6, 6, 7, 8], 3), ([7], 1), ([1, 2, 3, 4], 4),
             ([3, 3, 3], 1), ([1, 2, 2, 2, 3], 2), ([1, 2, 3, 4, 5, 6], 6), ([1, 1, 2, 2], 2)]
    for nums, k in cases:
        print(f"{nums}, k = {k} -> {str(can_divide_into_subsequences(nums, k)).lower()}")
    yes = check = 0
    for i in range(2000):
        n = next_random() % 100000 + 1 if i % 10 == 0 else next_random() % 1000 + 1
        top = next_random() % (n if i % 3 == 0 else 100000) + 1
        nums = random_sorted(n, top)
        k = next_random() % (n if i % 2 == 0 else min(20, n)) + 1
        r = can_divide_into_subsequences(nums, k)
        yes += r
        check = (check * 31 + (1 if r else 2) + n) % 1000000007
    print(f"2000 random arrays: {yes} can be divided, checksum {check}")


main()
