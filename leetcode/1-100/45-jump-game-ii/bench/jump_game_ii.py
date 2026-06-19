"""LeetCode #45 bench mirror — Python, the greedy range-expansion matcher (★).

Mirrors bench/jump_game_ii.kara: one cursor with farthest/current_end/jumps scalars,
collapsing the layered BFS into a single scan. Build a reachable array once, punch one slot per
iteration, fold the jump count into a rolling checksum. Same workload + sink as every other
mirror. The slow interpreted baseline (long-workload lane).
"""


def jump(nums: list[int], n: int) -> int:
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps


def main() -> None:
    total = 200000
    modulus = 1000000007
    n = 1000

    nums = [1 + (a % 4) for a in range(n)]

    acc = 0
    for k in range(total):
        nums[k % n] = 1 + (k % 9)
        ans = jump(nums, n)
        acc = (acc * 131 + ans) % modulus

    print(acc)


if __name__ == "__main__":
    main()
