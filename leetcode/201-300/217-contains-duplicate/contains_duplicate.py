"""LeetCode 217 — Contains Duplicate (Python mirror / oracle).

One linear pass with a set of seen values; true on the first repeat. Mirrors the
Kara version.
"""


def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def report(nums):
    print("true" if contains_duplicate(nums) else "false")


def main():
    report([1, 2, 3, 1])
    report([1, 2, 3, 4])
    report([1, 1, 1, 3, 3, 4, 3, 2, 4, 2])
    report([])
    report([1])
    report([-1, -1])
    report([-3, 0, 7, 9, -3])


main()
