"""LeetCode #39 bench mirror — Python, the mutable-path backtracking solver (★).

Mirrors bench/combination_sum.kara: index-bounded DFS with one mutable path (append/pop),
snapshotting (path.copy()) into a list-of-lists at each target-hit leaf. Same workload +
checksum as every other mirror — the slow interpreter foil for the seq lane.
"""

from __future__ import annotations

TOTAL = 30000
MODULUS = 1000000007
CANDIDATES = [2, 3, 5, 7]


def backtrack(start: int, remaining: int, path: list[int], out: list[list[int]]) -> None:
    if remaining == 0:
        out.append(path.copy())
        return
    n = len(CANDIDATES)
    i = start
    while i < n:
        c = CANDIDATES[i]
        if c <= remaining:
            path.append(c)
            backtrack(i, remaining - c, path, out)
            path.pop()
        i += 1


def combination_sum(target: int) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []
    backtrack(0, target, path, out)
    return out


def main() -> None:
    acc = 0
    for k in range(TOTAL):
        target = 18 + (k % 13)
        combos = combination_sum(target)

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
