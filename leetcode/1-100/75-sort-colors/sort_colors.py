"""LeetCode #75: Sort Colors — Dutch National Flag, one pass, O(1) space.

Mirror of sort_colors.kara. Three pointers partition the {0,1,2} array in place:
[0,low) are 0s, [low,mid) are 1s, [mid,high] unknown, (high,n) are 2s. The == 2
case does NOT advance mid (the value pulled from high is unclassified). Same
twelve cases and the same output shape (the sorted array per case, then a `sums:`
fold of a per-array polynomial hash) so the files diff line-for-line. (The
counting-sort variant lives only in Kāra; this mirror tracks the star.)
"""

from __future__ import annotations


def sort_colors(a: list[int]) -> None:
    n = len(a)
    if n == 0:
        return
    low, mid, high = 0, 0, n - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1


def print_arr(a: list[int]) -> None:
    print("[" + ", ".join(str(x) for x in a) + "]")


def hash_arr(a: list[int]) -> int:
    acc = 0
    for x in a:
        acc = (acc * 131 + x) % 1000000007
    return acc


def report(grid: list[int], acc: list[str]) -> None:
    a = list(grid)
    sort_colors(a)
    print_arr(a)
    acc.append(str(hash_arr(a)))


def main() -> None:
    acc: list[str] = []
    report([2, 0, 2, 1, 1, 0], acc)
    report([2, 0, 1], acc)
    report([0], acc)
    report([1], acc)
    report([2], acc)
    report([2, 2, 2], acc)
    report([0, 0, 0], acc)
    report([1, 1, 1], acc)
    report([0, 1, 2], acc)
    report([2, 1, 0], acc)
    report([2, 0, 1, 2, 1, 0, 0, 2, 1], acc)
    report([1, 0, 2, 0, 1, 2, 1, 0], acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
