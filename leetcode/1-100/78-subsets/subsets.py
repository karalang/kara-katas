"""LeetCode #78: Subsets — emit-at-every-node backtracking.

Mirror of subsets.kara. Start-indexed DFS over the power set: snapshot the path at
the top of each call (every node is a subset), then extend with nums[i] and recurse
at i+1. Emitting before the loop makes the empty set first and each prefix precede
its extensions, so the natural order is lexicographic. Same six cases and output
shape (a `subsets: count` header, each subset on its own line, then a `sums:` fold of
`count:hash` per case) so the files diff line-for-line. (The iterative variant lives
only in Kāra; this mirror tracks the star.)
"""

from __future__ import annotations


def backtrack(nums: list[int], start: int, path: list[int], out: list[list[int]]) -> None:
    out.append(path[:])                # every node is a subset
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(nums, i + 1, path, out)
        path.pop()


def subsets(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    backtrack(nums, 0, [], out)
    return out


def show(subset: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in subset) + "]"


def hash_subsets(subs: list[list[int]]) -> int:
    acc = 0
    for sub in subs:
        acc = (acc * 131 + (len(sub) + 1)) % 1000000007  # length marker
        for x in sub:
            acc = (acc * 131 + (x + 1)) % 1000000007
    return acc


def report(nums: list[int], acc: list[str]) -> None:
    subs = subsets(nums)
    count = len(subs)
    print(f"subsets: {count}")
    for sub in subs:
        print(show(sub))
    acc.append(f"{count}:{hash_subsets(subs)}")


def main() -> None:
    acc: list[str] = []
    report([1, 2, 3], acc)
    report([0], acc)
    report([1, 2], acc)
    report([2, 4, 6, 8, 10], acc)
    report([7], acc)
    report([1, 2, 3, 4], acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
