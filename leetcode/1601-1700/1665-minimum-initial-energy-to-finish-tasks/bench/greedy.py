"""Benchmark workload — greedy O(n log n) Minimum Initial Energy to Finish Tasks.

Algorithmic mirror of bench/greedy.kara. See ../README.md § Benchmarks
for the choice of N / K and the deterministic generator.
"""

from __future__ import annotations


def minimum_effort(tasks: list[tuple[int, int]]) -> int:
    ordered = sorted(tasks, key=lambda t: t[1] - t[0], reverse=True)
    energy = 0
    spent = 0
    for actual, minimum in ordered:
        need = spent + minimum
        if need > energy:
            energy = need
        spent += actual
    return energy


def main() -> None:
    N = 50_000
    data = [((i * 7) % 100 + 1, (i * 7) % 100 + 1 + (i * 13) % 50) for i in range(N)]

    sum_result = 0
    for _ in range(5):
        sum_result += minimum_effort(data)
    print(sum_result)


if __name__ == "__main__":
    main()
