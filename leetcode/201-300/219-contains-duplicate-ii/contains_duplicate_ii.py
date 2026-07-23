"""LeetCode 219 — Contains Duplicate II (Python mirror / oracle).

One pass with a dict from value to its most recent index; true when a repeat
falls within a gap of k. Mirrors the Kara version.
"""


def contains_nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False


def report(nums, k):
    print("true" if contains_nearby_duplicate(nums, k) else "false")


def main():
    a = [1, 2, 3, 1]
    report(a, 3)
    report([1, 0, 1, 1], 1)
    report([1, 2, 3, 1, 2, 3], 2)
    report(a, 2)
    report([1], 1)
    report([99, 99], 2)
    f = [4, 1, 2, 1, 4]
    report(f, 3)
    report(f, 1)


main()
