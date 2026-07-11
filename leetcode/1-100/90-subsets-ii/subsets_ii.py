"""LeetCode #90: Subsets II — sorted backtracking with skip-duplicates-at-level.

Mirror of subsets_ii.kara. Sort nums so equal values are adjacent, then in the DFS
take nums[i] only when i == start or nums[i] != nums[i-1] — so a run of equal values is
extended but never started twice at the same level, killing duplicate subsets. Otherwise
#78's emit-at-every-node backtracking. Same nine cases and output shape (a `subsets:
count` header, each subset on its own line, then a `sums:` fold of `count:hash` per case)
so the files diff line-for-line.
"""

from __future__ import annotations


def backtrack(nums: list[int], start: int, path: list[int], out: list[list[int]]) -> None:
    out.append(path[:])                        # every node is a subset
    for i in range(start, len(nums)):
        if i == start or nums[i] != nums[i - 1]:
            path.append(nums[i])
            backtrack(nums, i + 1, path, out)
            path.pop()


def subsets_with_dup(input_: list[int]) -> list[list[int]]:
    nums = sorted(input_)
    out: list[list[int]] = []
    backtrack(nums, 0, [], out)
    return out


def show(subset: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in subset) + "]"


def hash_subsets(subs: list[list[int]]) -> int:
    acc = 0
    for sub in subs:
        acc = (acc * 131 + (len(sub) + 1)) % 1000000007
        for x in sub:
            acc = (acc * 131 + (x + 1)) % 1000000007
    return acc


def report(input_: list[int], acc: list[str]) -> None:
    subs = subsets_with_dup(input_)
    count = len(subs)
    print(f"subsets: {count}")
    for sub in subs:
        print(show(sub))
    acc.append(f"{count}:{hash_subsets(subs)}")


def main() -> None:
    acc: list[str] = []
    report([1, 2, 2], acc)
    report([0], acc)
    report([4, 4, 4, 1, 4], acc)
    report([1, 1], acc)
    report([], acc)
    report([2, 1, 2], acc)
    report([5, 5, 5, 5], acc)
    report([3, 1, 4, 2], acc)
    report([-1, -1, 2], acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
