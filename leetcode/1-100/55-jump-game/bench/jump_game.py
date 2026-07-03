"""LeetCode #55 bench harness — Python, the greedy forward max-reach solver (★).

Mirror of jump_game.kara. See ../README.md § Benchmarks for what these numbers mean.

Workload: build a reachable array `nums` (length n, each entry in 1..4 so every index can always
step at least one forward — the last index is always reachable) ONCE, then TOTAL times punch a
single slot (`nums[k%n] = 1 + k%9`, a bigger reach) and run the greedy scan, which returns the
index at which it decided (here always the early-exit index where `farthest` first covers the
last index). That work-index is folded into a rolling checksum. The punches are NOT reverted, so
the array state carries forward and the answer varies with the loop index (no hoisting); the
checksum carries a loop-borne dependency, so this is a single-lane (seq) bench by construction.
Every language mirror folds the identical answer sequence and prints the identical checksum.
"""


def can_jump_work(nums: list[int], n: int) -> int:
    farthest = 0
    i = 0
    while i < n:
        if i > farthest:
            return i
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if farthest >= n - 1:
            return i
        i += 1
    return i


def main() -> None:
    total = 200000
    modulus = 1000000007
    n = 1000

    nums = [1 + (a % 4) for a in range(n)]

    acc = 0
    for k in range(total):
        nums[k % n] = 1 + (k % 9)
        ans = can_jump_work(nums, n)
        acc = (acc * 131 + ans) % modulus

    print(acc)


if __name__ == "__main__":
    main()
