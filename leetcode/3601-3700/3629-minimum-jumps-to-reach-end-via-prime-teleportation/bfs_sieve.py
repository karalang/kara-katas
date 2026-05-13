"""LeetCode #3629: Minimum Jumps to Reach End via Prime Teleportation.

Algorithmic mirror of bfs_sieve.kara — same merged-factors sieve, same per-prime
bucket, same one-shot bucket consumption during BFS. Output format matches
line-for-line so the two files can be diffed directly.
"""

from __future__ import annotations

from collections import defaultdict, deque


def build_factors(cap: int) -> list[list[int]]:
    """factors[k] = ascending distinct prime factors of k for k >= 2; [] for k < 2."""
    factors: list[list[int]] = [[] for _ in range(cap + 1)]
    for i in range(2, cap + 1):
        if not factors[i]:                      # i has no smaller prime stamped → i is prime
            for j in range(i, cap + 1, i):
                factors[j].append(i)
    return factors


def min_jumps(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0

    cap = max(max(nums), 1)
    factors = build_factors(cap)

    bucket: dict[int, list[int]] = defaultdict(list)
    for j, v in enumerate(nums):
        for p in factors[v]:                    # direct lookup — no per-call factorization
            bucket[p].append(j)

    visited = [False] * n
    visited[0] = True
    queue: deque[tuple[int, int]] = deque()
    queue.append((0, 0))

    while queue:
        i, d = queue.popleft()
        if i == n - 1:
            return d
        if i > 0 and not visited[i - 1]:
            visited[i - 1] = True
            queue.append((i - 1, d + 1))
        if i + 1 < n and not visited[i + 1]:
            visited[i + 1] = True
            queue.append((i + 1, d + 1))
        v = nums[i]
        # Teleport fires only when nums[i] is itself prime: smallest prime factor is v.
        if v >= 2 and factors[v][0] == v:
            for j in bucket.pop(v, ()):
                if not visited[j]:
                    visited[j] = True
                    queue.append((j, d + 1))

    return -1


def report(nums: list[int]) -> None:
    print(min_jumps(nums))


def main() -> None:
    report([1, 2, 4, 6])      # expect: 2
    report([2, 3, 4, 7, 9])   # expect: 2
    report([4, 6, 5, 8])      # expect: 3
    report([42])              # expect: 0


if __name__ == "__main__":
    main()
