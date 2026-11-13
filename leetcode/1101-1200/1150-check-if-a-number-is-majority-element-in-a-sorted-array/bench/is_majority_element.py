# LeetCode #1150: Check If a Number Is Majority Element in a Sorted Array
# -- the Python mirror of the ★ arm: the run's start by `bisect_left`, then
# the value n // 2 places on.
from bisect import bisect_left


def is_majority_element(nums, target):
    n = len(nums)
    first = bisect_left(nums, target)
    return first + n // 2 < n and nums[first + n // 2] == target


def main():
    seed = 1150

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def big():
        a = next_random()
        return (a * 32768 + next_random()) % 1000000000 + 1

    def make_list():
        copies = 450 + next_random() % 101
        v = big()
        nums = [v] * copies
        for _ in range(copies, 1000):
            nums.append(big())
        nums.sort()
        return nums

    lists = [make_list() for _ in range(64)]
    yes = 0
    check = 0
    for q in range(10000000):
        nums = lists[q % 64]
        kind = next_random() % 4
        if kind == 0:
            target = nums[next_random() % 1000]
        elif kind == 1:
            target = nums[500]
        elif kind == 2:
            target = nums[next_random() % 1000] + 1
        else:
            target = big()
        if is_majority_element(nums, target):
            yes += 1
            check = (check * 31 + q) % 1000000007
    print(f"10000000 queries over 64 lists of 1000 values: majority {yes}, checksum {check}")


main()
