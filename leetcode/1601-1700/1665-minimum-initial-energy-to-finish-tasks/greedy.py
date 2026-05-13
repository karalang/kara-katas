"""LeetCode #1665: Minimum Initial Energy to Finish Tasks — greedy O(n log n).

Algorithmic mirror of greedy.kara. Output format matches line-for-line so the
two can be diffed directly.
"""

from __future__ import annotations


def minimum_effort(tasks: list[tuple[int, int]]) -> int:
    # Sort by buffer (minimum - actual) descending. Exchange argument: for any
    # adjacent pair (i, j), order (i then j) keeps the peak requirement lower
    # iff minimum_i - actual_i >= minimum_j - actual_j.
    ordered = sorted(tasks, key=lambda t: t[1] - t[0], reverse=True)
    energy = 0
    spent = 0
    for actual, minimum in ordered:
        # Just before task k, current energy is (energy - spent). We require
        # energy - spent >= minimum, i.e. energy >= spent + minimum.
        need = spent + minimum
        if need > energy:
            energy = need
        spent += actual
    return energy


def report(tasks: list[tuple[int, int]]) -> None:
    print(minimum_effort(tasks))


def main() -> None:
    report([(1, 2), (2, 4), (4, 8)])                              # expect: 8
    report([(1, 3), (2, 4), (10, 11), (10, 12), (8, 9)])          # expect: 32
    report([(1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12)])   # expect: 27


if __name__ == "__main__":
    main()
