"""LeetCode #57: Insert Interval — single linear three-phase sweep, O(n).

Mirror of insert_interval.kara: same left / merge / right phase structure,
same closed-interval-touching semantics (`[1,3]` + `[3,5]` merge), same output
format (interval count, then each merged interval's two endpoints, one per
line) so the two files diff line-for-line.
"""


def insert_interval(
    intervals: list[tuple[int, int]], new_interval: tuple[int, int]
) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    n = len(intervals)
    new_start, new_end = new_interval
    i = 0

    # Phase 1 — intervals entirely to the left of the new one (no overlap).
    while i < n:
        cur = intervals[i]
        if cur[1] >= new_start:
            break
        result.append(cur)
        i += 1

    # Phase 2 — absorb every overlapping/touching interval, widening the
    # running (new_start, new_end) window.
    while i < n:
        cur = intervals[i]
        if cur[0] > new_end:
            break
        if cur[0] < new_start:
            new_start = cur[0]
        if cur[1] > new_end:
            new_end = cur[1]
        i += 1
    result.append((new_start, new_end))

    # Phase 3 — the untouched tail.
    while i < n:
        result.append(intervals[i])
        i += 1
    return result


def report(intervals: list[tuple[int, int]], new_interval: tuple[int, int]) -> None:
    merged = insert_interval(intervals, new_interval)
    print(len(merged))
    for m in merged:
        print(m[0])
        print(m[1])


def main() -> None:
    report([(1, 3), (6, 9)], (2, 5))                       # 2 / 1 5 / 6 9
    report([(1, 2), (3, 5), (6, 7), (8, 10), (12, 16)], (4, 8))  # 3 / 1 2 / 3 10 / 12 16
    report([], (5, 7))                                     # 1 / 5 7
    report([(3, 5), (7, 9)], (0, 1))                       # 3 / 0 1 / 3 5 / 7 9
    report([(1, 2), (3, 5)], (8, 10))                      # 3 / 1 2 / 3 5 / 8 10
    report([(1, 3)], (3, 6))                               # 1 / 1 6
    report([(3, 5)], (1, 3))                               # 1 / 1 5
    report([(1, 10)], (3, 5))                              # 1 / 1 10
    report([(2, 3), (5, 6), (8, 9)], (1, 10))              # 1 / 1 10
    report([(1, 2), (4, 5), (7, 8)], (2, 7))               # 1 / 1 8


if __name__ == "__main__":
    main()
