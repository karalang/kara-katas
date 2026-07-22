"""LeetCode 179 — Largest Number (Python mirror / oracle).

Sort the numbers-as-strings descending under the pairwise concatenation
comparator (a before b iff a+b >= b+a), join, and collapse the all-zeros case.
Insertion sort to mirror the Kāra version exactly.
"""


def sort_desc(strs):
    n = len(strs)
    for i in range(1, n):
        j = i
        while j > 0 and strs[j - 1] + strs[j] < strs[j] + strs[j - 1]:
            strs[j - 1], strs[j] = strs[j], strs[j - 1]
            j -= 1


def largest_number(nums):
    strs = [str(x) for x in nums]
    sort_desc(strs)
    if strs and strs[0] == "0":
        return "0"
    return "".join(strs)


def report(nums):
    print(largest_number(nums))


def main():
    report([10, 2])
    report([3, 30, 34, 5, 9])
    report([1])
    report([0, 0])
    report([999999998, 999999997, 999999999, 1])
    report([34323, 3432, 3])


main()
