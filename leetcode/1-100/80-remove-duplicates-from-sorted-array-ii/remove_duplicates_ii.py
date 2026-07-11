"""LeetCode #80: Remove Duplicates from Sorted Array II — two-pointer, in place.

Mirror of remove_duplicates_ii.kara. A write cursor k trails the read cursor i; a
value is kept only when it differs from the one two slots back in the written prefix
(`nums[i] != nums[k-2]`), so each value lands at most twice. Same seven cases and
output shape (a `k=<len>: [<prefix>]` line per case, then a `sink:` fold of length +
surviving prefix) so the files diff line-for-line.
"""

from __future__ import annotations


def remove_dups(nums: list[int]) -> int:
    n = len(nums)
    if n <= 2:
        return n
    k = 2
    for i in range(2, n):
        if nums[i] != nums[k - 2]:
            nums[k] = nums[i]
            k += 1
    return k


def report(vals: list[int], acc: list[int]) -> None:
    nums = list(vals)
    k = remove_dups(nums)
    print(f"k={k}: [" + ", ".join(str(nums[j]) for j in range(k)) + "]")
    a = (acc[0] * 131 + (k + 1)) % 1000000007
    for p in range(k):
        a = (a * 131 + (nums[p] + 1)) % 1000000007
    acc[0] = a


def main() -> None:
    acc = [0]
    report([1, 1, 1, 2, 2, 3], acc)
    report([0, 0, 1, 1, 1, 1, 2, 3, 3], acc)
    report([1, 2, 3], acc)
    report([1, 1], acc)
    report([7], acc)
    report([], acc)
    report([5, 5, 5, 5], acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
