"""Benchmark workload — Merge Intervals (LeetCode #56).

Python mirror of bench/merge_intervals.kara. Same LCG generator, per-case
(start, end) shape, sort-by-first-component + sweep, and sink. CPython is
multi-second per sample at K=1M, so this mirror runs K=100_000 (1/10th)
and the README quotes the projected ratio. M divides 100_000 evenly, so
each of the 8 cases is hit exactly 12_500 times.
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


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % 2147483648


def build_case(seed: int, count: int) -> list[tuple[int, int]]:
    v = []
    state = seed
    for _ in range(count):
        state = lcg_next(state)
        start = state % 51
        state = lcg_next(state)
        width = (state % 10) + 1
        v.append((start, start + width))
    return v


def main() -> None:
    m_cases = 8
    n_values = 16
    k_iters = 100_000

    sets = [build_case(m * 1000003 + 12345, n_values) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        r = merge_intervals(sets[idx])
        total += len(r)
    print(total)


if __name__ == "__main__":
    main()
