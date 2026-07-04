"""Benchmark workload — Permutation Sequence (LeetCode #60), NEXT-PERM solver.

Python mirror of bench/permutation_sequence_nextperm.kara. Same M=9 rotated
(n,k) cases, next_permutation iterated k-1 times (O(k·n)). This solver does
thousands of steps per case in pure Python, so this mirror runs K=9 (each case
exactly once); the README normalizes to permutations-resolved-per-second.
"""

NTAB = [9, 8, 9, 7, 8, 9, 6, 7, 9]
KTAB = [362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000]
M = 9


def next_permutation(a: list[int]) -> None:
    length = len(a)
    i = length - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = length - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    lo, hi = i + 1, length - 1
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1


def get_permutation(n: int, k: int) -> list[int]:
    a = list(range(1, n + 1))
    for _ in range(k - 1):
        next_permutation(a)
    return a


def checksum(perm: list[int], n: int) -> int:
    s = 0
    for i in range(n):
        s += perm[i] * (i + 1)
    return s


def main() -> None:
    k_iters = 9
    total = 0
    for k in range(k_iters):
        idx = k % M
        perm = get_permutation(NTAB[idx], KTAB[idx])
        total += checksum(perm, NTAB[idx])
    print(total)


if __name__ == "__main__":
    main()
