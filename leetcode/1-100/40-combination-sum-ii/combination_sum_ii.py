"""LeetCode #40: Combination Sum II — known-correct reference oracle.

Given candidates that MAY CONTAIN DUPLICATES and a `target`, return every unique
combination summing to `target` where each array element is used AT MOST ONCE and the
result has no duplicate combinations. The once-each, duplicate-input twin of #39: sort
first, recurse at i+1 (use once), and dedup repeated values at each tree level.

Three styles, all producing the IDENTICAL combination list for every case (cross-checked
below), each mirroring one Kāra pedagogical file:

  - Style 1 (sorted DFS + same-level duplicate skip, ★) — mirror of combination_sum_ii.kara
  - Style 2 (counted/grouped DFS over distinct values)   — mirror of combination_sum_ii_counted.kara
  - Style 3 (immutable-snapshot sorted DFS)               — mirror of combination_sum_ii_snapshot.kara

All emit combinations in the sorted lexicographic order; the output is
`target={t} -> {count}` followed by one `[a, b, c]` line per combination, line-for-line
diffable against each Kāra mirror's stdout under both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: sorted DFS + same-level duplicate skip (mirrors ..._ii.kara, ★) -----------

def combination_sum2_skip(candidates: list[int], target: int) -> list[list[int]]:
    cands = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path.copy())
            return
        n = len(cands)
        i = start
        while i < n:
            c = cands[i]
            if c > remaining:
                break
            if i > start and c == cands[i - 1]:
                i += 1
                continue
            path.append(c)
            backtrack(i + 1, remaining - c)  # i+1 — each element used once
            path.pop()
            i += 1

    backtrack(0, target)
    return out


# --- Style 2: counted/grouped DFS over distinct values (mirrors ..._ii_counted.kara) -----

def combination_sum2_counted(candidates: list[int], target: int) -> list[list[int]]:
    cands = sorted(candidates)
    vals: list[int] = []
    cnts: list[int] = []
    n = len(cands)
    i = 0
    while i < n:
        v = cands[i]
        j = i
        while j < n and cands[j] == v:
            j += 1
        vals.append(v)
        cnts.append(j - i)
        i = j

    out: list[list[int]] = []
    path: list[int] = []

    def dfs(idx: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path.copy())
            return
        if idx == len(vals):
            return
        v = vals[idx]
        k = cnts[idx]
        while k > 0 and k * v > remaining:
            k -= 1
        while k >= 0:  # descending copies → lexicographic order
            for _ in range(k):
                path.append(v)
            dfs(idx + 1, remaining - k * v)
            for _ in range(k):
                path.pop()
            k -= 1

    dfs(0, target)
    return out


# --- Style 3: immutable-snapshot sorted DFS (mirrors ..._ii_snapshot.kara) ----------------

def combination_sum2_snapshot(candidates: list[int], target: int) -> list[list[int]]:
    cands = sorted(candidates)
    out: list[list[int]] = []

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            out.append(path)
            return
        n = len(cands)
        i = start
        while i < n:
            c = cands[i]
            if c > remaining:
                break
            if i > start and c == cands[i - 1]:
                i += 1
                continue
            backtrack(i + 1, remaining - c, path + [c])
            i += 1

    backtrack(0, target, [])
    return out


def show(combo: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in combo) + "]"


def report(candidates: list[int], target: int) -> None:
    a = combination_sum2_skip(candidates, target)
    b = combination_sum2_counted(candidates, target)
    c = combination_sum2_snapshot(candidates, target)
    assert a == b == c, (candidates, target, a, b, c)
    print(f"target={target} -> {len(a)}")
    for combo in a:
        print(show(combo))
    print("---")


def main() -> None:
    report([10, 1, 2, 7, 6, 1, 5], 8)
    report([2, 5, 2, 1, 2], 5)
    report([2, 4, 6], 3)
    report([1, 1, 1, 1], 3)
    report([1, 1, 2, 2, 3, 3, 5], 6)


if __name__ == "__main__":
    main()
