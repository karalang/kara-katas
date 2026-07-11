"""LeetCode #77: Combinations — mutable-path backtracking over a start index.

Mirror of combinations.kara. DFS over a start index picks k distinct numbers from
[1, n]: pick value i, recurse with start = i+1 (used at most once), snapshot the
path when it reaches length k. Same eight cases and output shape (a
`combine(n,k): count` header, each combination on its own line, then a `sums:` fold
of `count:hash` per case) so the files diff line-for-line. (The pruned variant lives
only in Kāra; this mirror tracks the star.)
"""

from __future__ import annotations


def backtrack(n: int, k: int, start: int, path: list[int], out: list[list[int]]) -> None:
    if len(path) == k:
        out.append(path[:])
        return
    for i in range(start, n + 1):
        path.append(i)
        backtrack(n, k, i + 1, path, out)
        path.pop()


def combine(n: int, k: int) -> list[list[int]]:
    out: list[list[int]] = []
    backtrack(n, k, 1, [], out)
    return out


def show(combo: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in combo) + "]"


def hash_combos(combos: list[list[int]]) -> int:
    acc = 0
    for combo in combos:
        for x in combo:
            acc = (acc * 131 + x) % 1000000007
    return acc


def report(n: int, k: int, acc: list[str]) -> None:
    combos = combine(n, k)
    count = len(combos)
    print(f"combine({n},{k}): {count}")
    for combo in combos:
        print(show(combo))
    acc.append(f"{count}:{hash_combos(combos)}")


def main() -> None:
    acc: list[str] = []
    report(4, 2, acc)
    report(1, 1, acc)
    report(3, 3, acc)
    report(5, 1, acc)
    report(4, 4, acc)
    report(5, 2, acc)
    report(6, 3, acc)
    report(4, 0, acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
