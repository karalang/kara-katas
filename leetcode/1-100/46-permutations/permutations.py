"""LeetCode #46: Permutations — known-correct reference oracle.

Given an array of DISTINCT integers `nums`, return every ordering of all the elements (there
are n! of them). Order is the answer, so unlike the combination katas there is no index-monotone
walk: every level of the DFS may pick any element not yet used on the current branch. Scanning
the indices `0..n` in order and picking the first available index first yields the canonical
"lexicographic by original index" listing — for [1,2,3]: [1,2,3],[1,3,2],[2,1,3],[2,3,1],
[3,1,2],[3,2,1], exactly LeetCode's order.

Three styles, all producing the IDENTICAL permutation list for every case (cross-checked
below), each mirroring one Kāra pedagogical file:

  - Style 1 (used-array, mutable path, ★)         — mirror of permutations.kara
  - Style 2 (in-path membership scan, mutable path) — mirror of permutations_scan.kara
  - Style 3 (immutable-snapshot DFS)               — mirror of permutations_snapshot.kara

The output is `[a, b, c] -> {count}` (the input echoed, then the count) followed by one
`[a, b, c]` line per permutation, line-for-line diffable against each Kāra mirror's stdout under
both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: used-array, mutable path (mirrors permutations.kara, ★) --------------------
#
# Carry one mutable `path` plus a parallel `used` marker; bracket each choice with
# mark/append … pop/unmark. At the leaf (path full) snapshot the path into the output.

def permute_used(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    out: list[list[int]] = []
    path: list[int] = []
    used = [False] * n

    def backtrack() -> None:
        if len(path) == n:
            out.append(path.copy())
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

    backtrack()
    return out


# --- Style 2: in-path membership scan (mirrors permutations_scan.kara) -------------------
#
# No side array: an element is available iff it is not already in `path` (linear scan).
# Distinct values make "value not in path" equivalent to "index not used".

def permute_scan(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack() -> None:
        if len(path) == n:
            out.append(path.copy())
            return
        for i in range(n):
            x = nums[i]
            if x not in path:
                path.append(x)
                backtrack()
                path.pop()

    backtrack()
    return out


# --- Style 3: immutable-snapshot DFS (mirrors permutations_snapshot.kara) ----------------
#
# Carry the path as an immutable snapshot; each descent builds a fresh child path
# (copy + append) and never undoes. The leaf snapshot IS the answer.

def permute_snapshot(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    out: list[list[int]] = []

    def backtrack(path: list[int]) -> None:
        if len(path) == n:
            out.append(path)
            return
        for i in range(n):
            x = nums[i]
            if x not in path:
                backtrack(path + [x])

    backtrack([])
    return out


def show(perm: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in perm) + "]"


def report(nums: list[int]) -> None:
    a = permute_used(nums)
    b = permute_scan(nums)
    c = permute_snapshot(nums)
    assert a == b == c, (nums, a, b, c)
    print(f"{show(nums)} -> {len(a)}")
    for perm in a:
        print(show(perm))
    print("---")


def main() -> None:
    report([1, 2, 3])
    report([0, 1])
    report([1])
    report([5, 3, 4])
    report([1, 2, 3, 4])


if __name__ == "__main__":
    main()
