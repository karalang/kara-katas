"""Benchmark workload — BFS + sieve solution to LeetCode #3629.

Algorithmic mirror of bench/bfs_sieve.kara. See ../README.md § Benchmarks
for the choice of N / K and the deterministic seeding scheme.
"""

from __future__ import annotations

from collections import defaultdict, deque


def build_factors(cap: int) -> list[list[int]]:
    factors: list[list[int]] = [[] for _ in range(cap + 1)]
    for i in range(2, cap + 1):
        if not factors[i]:
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
        for p in factors[v]:
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
        if v >= 2 and factors[v][0] == v:
            for j in bucket.pop(v, ()):
                if not visited[j]:
                    visited[j] = True
                    queue.append((j, d + 1))

    return -1


def main() -> None:
    N = 50_000
    data = [(i * 7919 + 13) % 999983 + 2 for i in range(N)]

    sum_result = 0
    for _ in range(50):
        sum_result += min_jumps(data)
    print(sum_result)


if __name__ == "__main__":
    main()
