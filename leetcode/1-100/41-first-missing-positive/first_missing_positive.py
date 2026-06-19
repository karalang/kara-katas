"""LeetCode #41: First Missing Positive — known-correct reference oracle.

Return the smallest positive integer absent from an unsorted array, in O(n) time. The
answer is always in [1, n+1]: a length-n array holds at most n distinct positives 1..n, so
either some value in 1..n is missing (the smallest such gap) or all are present (n+1).

Three styles, all returning the IDENTICAL answer for every case (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (in-place cyclic sort: index = value-1 home, ★) — mirror of first_missing_positive.kara
  - Style 2 (in-place sign marking: negation = present-bit)  — mirror of first_missing_positive_sign.kara
  - Style 3 (boolean seen-table, O(n) space)                 — mirror of first_missing_positive_seen.kara

Each `solve` takes a fresh copy of the input (the in-place styles mutate it). The output is
the bare answer per case, line-for-line diffable against each Kāra mirror's stdout under
both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: in-place cyclic sort (mirrors first_missing_positive.kara, ★) --------------
#
# Send each in-range value v to its home index v-1 by swapping, until the slot holds an
# out-of-range or already-home value. The `nums[v-1] != v` guard caps total swaps at n
# (each places one value permanently). The first slot not holding its home is the gap.

def fmp_cyclic(nums: list[int]) -> int:
    a = nums[:]  # do not mutate the caller's list
    n = len(a)
    i = 0
    while i < n:
        v = a[i]
        if 1 <= v <= n and a[v - 1] != v:
            a[v - 1], a[i] = v, a[v - 1]  # swap; re-examine i (don't advance)
        else:
            i += 1
    for j in range(n):
        if a[j] != j + 1:
            return j + 1
    return n + 1


# --- Style 2: in-place sign marking (mirrors first_missing_positive_sign.kara) ------------
#
# Use the sign of slot v-1 as the "is v present?" bit. Neutralize out-of-range values to
# n+1, then for each magnitude v in [1,n] negate slot v-1 (once). The first still-positive
# slot is the missing value.

def fmp_sign(nums: list[int]) -> int:
    a = nums[:]
    n = len(a)
    for i in range(n):
        if a[i] <= 0 or a[i] > n:
            a[i] = n + 1
    for i in range(n):
        v = abs(a[i])
        if 1 <= v <= n and a[v - 1] > 0:
            a[v - 1] = -a[v - 1]
    for j in range(n):
        if a[j] > 0:
            return j + 1
    return n + 1


# --- Style 3: boolean seen-table, O(n) space (mirrors first_missing_positive_seen.kara) ---
#
# The straightforward presence table: mark seen[v] for in-range v, return the first unseen
# value in 1..=n. Leaves the input intact; O(n) extra space.

def fmp_seen(nums: list[int]) -> int:
    n = len(nums)
    seen = [False] * (n + 1)
    for v in nums:
        if 1 <= v <= n:
            seen[v] = True
    for v in range(1, n + 1):
        if not seen[v]:
            return v
    return n + 1


def report(nums: list[int]) -> None:
    a = fmp_cyclic(nums)
    b = fmp_sign(nums)
    c = fmp_seen(nums)
    assert a == b == c, (nums, a, b, c)
    print(a)


def main() -> None:
    report([1, 2, 0])
    report([3, 4, -1, 1])
    report([7, 8, 9, 11, 12])
    report([1])
    report([2, 2, 2, 2])
    report([1, 2, 3, 4, 5])
    report([-5, -3, -1])
    report([5, 3, 1, 2, 6, 5])


if __name__ == "__main__":
    main()
