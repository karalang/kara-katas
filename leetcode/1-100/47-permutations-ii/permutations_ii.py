"""LeetCode #47: Permutations II — known-correct reference oracle.

Given an array `nums` that MAY CONTAIN DUPLICATES, return every UNIQUE ordering of all its
elements. This is the duplicate-input twin of kata #46 (distinct integers): #46's any-unused-element
DFS already emitted each ordering once, but with repeated values it emits the same ordering once per
arrangement of the equal copies, so the duplicate siblings must be suppressed. The canonical fix is
the kata-40 move: SORT first, then at each tree level skip a candidate equal to its predecessor when
that predecessor is not currently consumed on the branch. Sorting also flips the output order versus
#46: permutations come out lexicographic BY VALUE — for [1,1,2]: [1,1,2],[1,2,1],[2,1,1].

Four styles, all producing the IDENTICAL unique-permutation list for every case (cross-checked
below), each mirroring one Kāra pedagogical file:

  - Style 1 (sorted + used-array, adjacent-duplicate skip, ★) — mirror of permutations_ii.kara
  - Style 2 (counted/grouped DFS over distinct values)        — mirror of permutations_ii_counted.kara
  - Style 3 (immutable-snapshot, shrinking remaining-multiset) — mirror of permutations_ii_snapshot.kara
  - Style 4 (in-place swap DFS with a per-level seen-set)     — mirror of permutations_ii_swap.kara

The output is `[a, b, c] -> {count}` (the input echoed, then the count) followed by one
`[a, b, c]` line per permutation, line-for-line diffable against each Kāra mirror's stdout under
both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: sorted + used-array, adjacent-duplicate skip (mirrors permutations_ii.kara, ★) ---
#
# Sort, carry one mutable `path` plus a parallel `used` marker; bracket each choice with
# mark/append … pop/unmark. Skip `nums[i] == nums[i-1] and not used[i-1]` to suppress duplicate
# siblings. At the leaf (path full) snapshot the path into the output.

def permute_unique_used(nums: list[int]) -> list[list[int]]:
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


# --- Style 2: counted/grouped DFS (mirrors permutations_ii_counted.kara) -------------------------
#
# Sort, run-group into distinct (value, count) pairs. Fill positions one at a time; at each position
# offer each distinct value with a positive remaining count (decrement / recurse / increment).
# Each value is offered at most once per level, so duplicate permutations are impossible — no
# adjacent skip, no per-index used array.

def permute_unique_counted(nums: list[int]) -> list[list[int]]:
    xs = sorted(nums)
    n = len(xs)
    vals: list[int] = []
    cnts: list[int] = []
    i = 0
    while i < n:
        v = xs[i]
        j = i
        while j < n and xs[j] == v:
            j += 1
        vals.append(v)
        cnts.append(j - i)
        i = j

    out: list[list[int]] = []
    path: list[int] = []

    def dfs(depth: int) -> None:
        if depth == n:
            out.append(path.copy())
            return
        for k in range(len(vals)):
            if cnts[k] > 0:
                cnts[k] -= 1
                path.append(vals[k])
                dfs(depth + 1)
                path.pop()
                cnts[k] += 1

    dfs(0)
    return out


# --- Style 3: immutable-snapshot, shrinking remaining-multiset (mirrors permutations_ii_snapshot.kara) ---
#
# Carry both the chosen prefix and the still-available (sorted) multiset as immutable snapshots;
# each descent removes one element and appends one, never undoing. The leaf (remaining empty) IS
# the answer. Unconditional adjacent skip dedups siblings (consumed elements are gone from
# `remaining`, so a duplicate predecessor is always a same-level sibling).

def permute_unique_snapshot(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []

    def backtrack(remaining: list[int], path: list[int]) -> None:
        if not remaining:
            out.append(path)
            return
        for i in range(len(remaining)):
            if i > 0 and remaining[i] == remaining[i - 1]:
                continue
            rest = remaining[:i] + remaining[i + 1:]
            backtrack(rest, path + [remaining[i]])

    backtrack(sorted(nums), [])
    return out


# --- Style 4: in-place swap DFS with a per-level seen-set (mirrors permutations_ii_swap.kara) ---
#
# Permute the array in place — fix each distinct still-available value into position `start` by
# swapping, recurse, swap back. No sort, so dedup is a per-level `seen` set (the canonical
# alternative to sort + adjacent skip). Swap order is arbitrary, so the result is sorted to the
# canonical lexicographic-by-value listing before returning.

def permute_unique_swap(nums: list[int]) -> list[list[int]]:
    xs = list(nums)
    n = len(xs)
    out: list[list[int]] = []

    def dfs(start: int) -> None:
        if start == n:
            out.append(xs.copy())
            return
        seen: set[int] = set()
        for i in range(start, n):
            if xs[i] in seen:
                continue
            seen.add(xs[i])
            xs[start], xs[i] = xs[i], xs[start]
            dfs(start + 1)
            xs[start], xs[i] = xs[i], xs[start]

    dfs(0)
    out.sort()
    return out


def show(perm: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in perm) + "]"


def report(nums: list[int]) -> None:
    a = permute_unique_used(nums)
    b = permute_unique_counted(nums)
    c = permute_unique_snapshot(nums)
    d = permute_unique_swap(nums)
    assert a == b == c == d, (nums, a, b, c, d)
    print(f"{show(nums)} -> {len(a)}")
    for perm in a:
        print(show(perm))
    print("---")


def main() -> None:
    report([1, 1, 2])
    report([1, 2, 3])
    report([2, 2, 1, 1])
    report([3, 3, 0, 3])
    report([1])
    report([5, 5, 5])


if __name__ == "__main__":
    main()
