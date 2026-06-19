"""LeetCode #40 bench mirror — Python, the sorted same-level-dedup backtracker (★).

Mirrors bench/combination_sum_ii.kara: sort once, index-bounded DFS at i+1 with the
same-level duplicate skip and suffix break, snapshotting (path.copy()) into a list-of-lists
at each leaf. Same workload + checksum as every other mirror — the slow interpreter foil.
"""

from __future__ import annotations

TOTAL = 30000
MODULUS = 1000000007
CANDIDATES = sorted([1, 1, 2, 2, 3, 3, 4, 5, 6, 7])


def backtrack(start: int, remaining: int, path: list[int], out: list[list[int]]) -> None:
    if remaining == 0:
        out.append(path.copy())
        return
    n = len(CANDIDATES)
    i = start
    while i < n:
        c = CANDIDATES[i]
        if c > remaining:
            break
        if i > start and c == CANDIDATES[i - 1]:
            i += 1
            continue
        path.append(c)
        backtrack(i + 1, remaining - c, path, out)
        path.pop()
        i += 1


def combination_sum2(target: int) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []
    backtrack(0, target, path, out)
    return out


def main() -> None:
    acc = 0
    for k in range(TOTAL):
        target = 10 + (k % 13)
        combos = combination_sum2(target)

        sig = 0
        for combo in combos:
            s = 0
            for i in range(len(combo)):
                s += combo[i] * (i + 1)
            sig = (sig * 31 + s) % MODULUS
        sig = (sig + len(combos)) % MODULUS
        acc = (acc * 131 + sig) % MODULUS

    print(acc)


if __name__ == "__main__":
    main()
