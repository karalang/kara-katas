"""LeetCode 215 — Kth Largest Element in an Array (Python mirror / oracle).

Deterministic quickselect (Lomuto partition, last-element pivot): the k-th
largest is at ascending index n-k. Mirrors the Kara version.
"""


def partition(a, lo, hi):
    pivot = a[hi]
    i = lo
    j = lo
    while j < hi:
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
        j += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quickselect(a, lo, hi, target):
    if lo == hi:
        return a[lo]
    p = partition(a, lo, hi)
    if p == target:
        return a[p]
    if target < p:
        return quickselect(a, lo, p - 1, target)
    return quickselect(a, p + 1, hi, target)


def find_kth_largest(nums, k):
    a = list(nums)
    n = len(a)
    return quickselect(a, 0, n - 1, n - k)


def report(nums, k):
    print(find_kth_largest(nums, k))


def main():
    report([3, 2, 1, 5, 6, 4], 2)
    report([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
    report([1], 1)
    report([2, 1], 2)
    report([7, 6, 5, 4, 3, 2, 1], 3)
    report([1, 2, 3, 4, 5, 6], 1)
    report([5, 5, 5, 5], 2)
    report([-1, -5, 3, 0, 2], 1)
    report([-1, -5, 3, 0, 2], 5)


main()
