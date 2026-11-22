# LeetCode #2733: Neither Minimum nor Maximum -- Python mirror of
# neither.kara (the ★ arm): the least and the greatest in one pass, then
# the first number that is neither.


def find_non_min_or_max(nums):
    low = high = nums[0]
    for x in nums:
        low = min(low, x)
        high = max(high, x)
    for x in nums:
        if x != low and x != high:
            return x
    return -1


seed = 2733


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_numbers(n):
    every = list(range(1, 101))
    for i in range(99, 0, -1):
        j = next_random() % (i + 1)
        every[i], every[j] = every[j], every[i]
    return every[:n]


def is_right(nums, answer):
    low, high = min(nums), max(nums)
    some = any(x != low and x != high for x in nums)
    if answer == -1:
        return not some
    return answer in nums and answer != low and answer != high


def main():
    print("true" if is_right([3, 2, 1, 4], find_non_min_or_max([3, 2, 1, 4])) else "false")
    print(find_non_min_or_max([1, 2]))
    print(find_non_min_or_max([2, 1, 3]))
    found = wrong = check = 0
    for _ in range(5000):
        n = next_random() % 3 + 1 if next_random() % 4 == 0 else next_random() % 100 + 1
        nums = random_numbers(n)
        answer = find_non_min_or_max(nums)
        named = 0 if answer == -1 else 1
        if not is_right(nums, answer):
            wrong += 1
        found += named
        check = (check * 31 + named) % 1000000007
    print(f"5000 arrays: {found} with an answer, {wrong} wrong, checksum {check}")


main()
