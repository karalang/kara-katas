"""LeetCode 169 — Majority Element (Python mirror / oracle).

Boyer-Moore voting: a running candidate/count; +1 on a match, -1 otherwise, and
adopt a new candidate whenever the count reaches 0. O(n) time, O(1) space.
Mirrors the Kāra version.
"""


def majority_element(nums):
    candidate = nums[0]
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
        if x == candidate:
            count += 1
        else:
            count -= 1
    return candidate


def report(nums):
    print(majority_element(nums))


def main():
    report([3, 2, 3])
    report([2, 2, 1, 1, 1, 2, 2])
    report([7])
    report([5, 5, 5, 1, 1])
    report([-1, -1, -1, 2, 2, -1])


main()
