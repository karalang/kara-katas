"""LeetCode #39: Combination Sum — known-correct reference oracle.

Given DISTINCT positive integers `candidates` and a `target`, return every unique
combination that sums to `target`; the SAME candidate may be reused any number of times,
and a combination is a multiset of choices (order-insensitive). Uniqueness comes from an
index-bounded DFS: each call picks `candidates[start:]` and a pick of `candidates[i]`
recurses with `start = i` (reuse allowed) without ever looking left of `i`, so each
multiset is visited exactly once — no dedup set needed.

Three styles, all producing the IDENTICAL combination list for every case (cross-checked
below), each mirroring one Kāra pedagogical file:

  - Style 1 (mutable-path DFS, per-candidate prune, ★) — mirror of combination_sum.kara
  - Style 2 (immutable-snapshot DFS)                    — mirror of combination_sum_snapshot.kara
  - Style 3 (sorted candidates + early-break prune)     — mirror of combination_sum_sorted.kara

The test inputs are pre-sorted ascending, so all three emit combinations in the same DFS
order; the output is `target={t} -> {count}` followed by one `[a, b, c]` line per
combination, line-for-line diffable against each Kāra mirror's stdout under both
`karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: mutable-path DFS, per-candidate prune (mirrors combination_sum.kara, ★) ---
#
# Carry one mutable `path`; bracket each choice with append/pop. At the leaf (remaining
# == 0) snapshot the path into the output. A candidate is descended into only when it
# can't overshoot (`c <= remaining`) — the per-candidate prune.

def combination_sum_mutable(candidates: list[int], target: int) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path.copy())
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c <= remaining:
                path.append(c)
                backtrack(i, remaining - c)  # i, not i+1 — reuse allowed
                path.pop()

    backtrack(0, target)
    return out


# --- Style 2: immutable-snapshot DFS (mirrors combination_sum_snapshot.kara) -------------
#
# Carry the path as an immutable snapshot; each descent builds a fresh child path
# (copy + append) and never undoes. The leaf snapshot IS the answer.

def combination_sum_snapshot(candidates: list[int], target: int) -> list[list[int]]:
    out: list[list[int]] = []

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            out.append(path)
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c <= remaining:
                backtrack(i, remaining - c, path + [c])

    backtrack(0, target, [])
    return out


# --- Style 3: sorted candidates + early-break prune (mirrors combination_sum_sorted.kara) -
#
# Sort ascending so `candidates[i] > remaining` ends the loop (every later candidate is
# also too big) — a suffix cut where Style 1 filters per-candidate. Same mutable path.

def combination_sum_sorted(candidates: list[int], target: int) -> list[list[int]]:
    cands = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path.copy())
            return
        for i in range(start, len(cands)):
            c = cands[i]
            if c > remaining:
                break  # sorted ⇒ all later candidates overshoot too
            path.append(c)
            backtrack(i, remaining - c)
            path.pop()

    backtrack(0, target)
    return out


def show(combo: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in combo) + "]"


def report(candidates: list[int], target: int) -> None:
    a = combination_sum_mutable(candidates, target)
    b = combination_sum_snapshot(candidates, target)
    c = combination_sum_sorted(candidates, target)
    assert a == b == c, (candidates, target, a, b, c)
    print(f"target={target} -> {len(a)}")
    for combo in a:
        print(show(combo))
    print("---")


def main() -> None:
    report([2, 3, 6, 7], 7)
    report([2, 3, 5], 8)
    report([2], 1)
    report([2], 6)
    report([2, 3, 5], 12)


if __name__ == "__main__":
    main()
