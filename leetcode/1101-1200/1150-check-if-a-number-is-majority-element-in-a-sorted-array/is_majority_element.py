# LeetCode #1150: Check If a Number Is Majority Element in a Sorted Array
# -- the Python mirror of the ★ arm: the target's run starts at the first
# index whose value is not below it, and the target fills more than half
# the list exactly when it is still the value n // 2 places further on.
from bisect import bisect_left


def is_majority_element(nums, target):
    n = len(nums)
    first = bisect_left(nums, target)
    return first + n // 2 < n and nums[first + n // 2] == target


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    return (next_random() * 32768 + next_random()) % 1000000000 + 1


def problem(kind):
    n = 1 + next_random() % 60
    nums = []
    target = 0
    if kind == 0:
        for _ in range(n):
            nums.append(1 + next_random() % 3)
        target = 1 + next_random() % 4
    elif kind == 1:
        for _ in range(n):
            nums.append(big())
        target = nums[next_random() % n]
    elif kind == 2:
        target = 2 + big() % 999999998
        copies = min(max(n // 2 + next_random() % 3 - 1, 0), n)
        nums += [target] * copies
        for _ in range(copies, n):
            if next_random() % 2 == 0:
                nums.append(1 + next_random() % (target - 1))
            else:
                nums.append(target + 1 + next_random() % (1000000000 - target))
    else:
        for _ in range(n):
            nums.append(1 + next_random() % 2)
    nums.sort()
    if kind == 3:
        target = nums[n // 2]
    return nums, target


def b(x):
    return "true" if x else "false"


def show(nums, target):
    print(f"nums = {nums}, target = {target}  ->  {b(is_majority_element(nums, target))}")


def run(target, count, at):
    return [target - 1 if i < at else target if i < at + count else target + 1 for i in range(1000)]


def main():
    global seed
    show([2, 4, 5, 5, 5, 5, 5, 6, 6], 5)
    show([10, 100, 101, 101], 101)
    show([7], 7)
    show([7], 8)
    show([1, 1, 2, 2], 1)
    show([1, 1, 2, 2], 2)
    show([1, 2, 2], 2)
    show([1, 1, 2], 1)
    show([3, 3, 3], 1)
    show([3, 3, 3], 9)
    seed = 1150
    yes = 0
    check = 0
    for i in range(2000):
        nums, target = problem(i % 4)
        m = is_majority_element(nums, target)
        yes += m
        check = (check * 31 + (2 if m else 1)) % 1000000007
    print(f"2000 random lists: majority {yes}, checksum {check}")
    print(f"1000 copies of 10^9, target 10^9  ->  {b(is_majority_element([1000000000] * 1000, 1000000000))}")
    for count, at in [(501, 0), (501, 499), (501, 250), (500, 0), (500, 500), (500, 250)]:
        print(f"{count} copies of 7 from index {at} of 1000  ->  {b(is_majority_element(run(7, count, at), 7))}")


main()
