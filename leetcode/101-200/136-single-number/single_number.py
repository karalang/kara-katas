"""LeetCode 136 — Single Number (Python mirror / oracle).

XOR-fold: paired values cancel (a ^ a == 0), leaving the lone element.
"""


def single_number(nums):
    acc = 0
    for x in nums:
        acc ^= x
    return acc


def main():
    print(single_number([4, 1, 2, 1, 2]))
    print(single_number([2, 2, 1]))
    print(single_number([-7]))


main()
