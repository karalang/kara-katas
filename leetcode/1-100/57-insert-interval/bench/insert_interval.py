"""Benchmark workload — Insert Interval (LeetCode #57).

Python mirror of bench/insert_interval.kara. Same LCG generator, cursor-based
disjoint-sorted case builder, per-case new interval, linear three-phase
insert, and sink. CPython is multi-second per sample at K=1M, so this mirror
runs K=100_000 (1/10th) and the README quotes the projected ratio. M divides
100_000 evenly, so each of the 8 cases is hit exactly 12_500 times.
"""


def insert_interval(
    intervals: list[tuple[int, int]], new_interval: tuple[int, int]
) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    n = len(intervals)
    new_start, new_end = new_interval
    i = 0

    # Phase 1 — intervals entirely left of the new one.
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1
    # Phase 2 — absorb every overlapping/touching interval.
    while i < n and intervals[i][0] <= new_end:
        if intervals[i][0] < new_start:
            new_start = intervals[i][0]
        if intervals[i][1] > new_end:
            new_end = intervals[i][1]
        i += 1
    result.append((new_start, new_end))
    # Phase 3 — the untouched tail.
    while i < n:
        result.append(intervals[i])
        i += 1
    return result


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % 2147483648


def build_case(seed: int, count: int) -> list[tuple[int, int]]:
    v = []
    state = seed
    cursor = 0
    for _ in range(count):
        state = lcg_next(state)
        gap = (state % 4) + 2
        state = lcg_next(state)
        width = (state % 6) + 1
        start = cursor + gap
        end = start + width
        v.append((start, end))
        cursor = end
    return v


def pick_new(case: list[tuple[int, int]], m: int, count: int) -> tuple[int, int]:
    half = count // 2
    st = lcg_next(m * 7919 + 101)
    lo = st % half
    st = lcg_next(st)
    span = st % half
    hi = lo + 1 + span
    if hi > count - 1:
        hi = count - 1
    return (case[lo][0], case[hi][1])


def main() -> None:
    m_cases = 8
    n_values = 16
    k_iters = 100_000

    sets = [build_case(m * 1000003 + 12345, n_values) for m in range(m_cases)]
    news = [pick_new(sets[m], m, n_values) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        r = insert_interval(sets[idx], news[idx])
        total += len(r)
    print(total)


if __name__ == "__main__":
    main()
