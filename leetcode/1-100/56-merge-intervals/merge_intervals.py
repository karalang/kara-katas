"""LeetCode #56: Merge Intervals — sort + linear sweep, O(n log n).

Mirror of merge_intervals.kara: same sort-by-first-component + sweep shape,
same closed-interval-touching semantics (`[1,4]` + `[4,5]` merge), same
output format (interval count, then each merged interval's two endpoints,
one per line) so the two files diff line-for-line.
"""


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    s = sorted(intervals, key=lambda x: x[0])
    result: list[tuple[int, int]] = []
    n = len(s)
    if n == 0:
        return result
    cur_start, cur_end = s[0]
    for i in range(1, n):
        start_i, end_i = s[i]
        if start_i <= cur_end:
            if end_i > cur_end:
                cur_end = end_i
        else:
            result.append((cur_start, cur_end))
            cur_start, cur_end = start_i, end_i
    result.append((cur_start, cur_end))
    return result


def report(intervals: list[tuple[int, int]]) -> None:
    merged = merge_intervals(intervals)
    print(len(merged))
    for m in merged:
        print(m[0])
        print(m[1])


def main() -> None:
    report([(1, 3), (2, 6), (8, 10), (15, 18)])            # 3 / 1 6 / 8 10 / 15 18
    report([(1, 4), (4, 5)])                                # 1 / 1 5
    report([(5, 7)])                                        # 1 / 5 7
    report([(1, 2), (3, 4), (5, 6)])                        # 3 / 1 2 / 3 4 / 5 6
    report([(1, 10), (2, 5), (3, 7)])                       # 1 / 1 10
    report([(8, 10), (1, 3), (2, 6)])                       # 2 / 1 6 / 8 10
    report([(1, 10), (2, 3), (4, 5)])                       # 1 / 1 10
    report([(1, 3), (3, 5)])                                # 1 / 1 5
    report([(1, 5), (1, 5), (1, 5)])                        # 1 / 1 5


if __name__ == "__main__":
    main()
