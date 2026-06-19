"""LeetCode #47 bench mirror — Python, the sorted used-array adjacent-skip backtracker (★).

Mirrors bench/permutations_ii.kara: sort a working copy, then a DFS that picks any still-unused
element (tracked by a `used` bool list) with a same-level adjacent-duplicate skip, snapshotting the
path into a list-of-lists at each leaf. Same workload (TOTAL permutations of a fixed n=8 multiset
from {1,2,3,4}, one slot punched per iteration) and the same position-weighted checksum as every
other mirror. Runs the identical algorithm interpreted; prints the same sink.
"""

from __future__ import annotations


def permute_unique(nums: list[int]) -> list[list[int]]:
    xs = sorted(nums)
    n = len(xs)
    out: list[list[int]] = []
    path: list[int] = []
    used = [False] * n

    def backtrack() -> None:
        if len(path) == n:
            out.append(path.copy())
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and xs[i] == xs[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(xs[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return out


def main() -> None:
    total = 600
    modulus = 1000000007
    n = 8
    nums = [1 + (b % 4) for b in range(n)]

    acc = 0
    for k in range(total):
        nums[k % n] = 1 + (k % 4)
        perms = permute_unique(nums)

        sig = 0
        for perm in perms:
            s = 0
            for i in range(len(perm)):
                s += perm[i] * (i + 1)
            sig = (sig * 31 + s) % modulus
        sig = (sig + len(perms)) % modulus
        acc = (acc * 131 + sig) % modulus

    print(acc)


if __name__ == "__main__":
    main()
