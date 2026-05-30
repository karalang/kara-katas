"""Benchmark workload — 3Sum Closest (LeetCode #16).

Python mirror of bench/three_sum_closest.kara. Same LCG generator, per-case
target bag, sort + two-pointer body, and sink. CPython is multi-second per
sample at K=1M, so this mirror runs K=100_000 (1/10th) and the README quotes
the projected ratio. M divides 100_000 evenly, so each of the 8 cases is hit
exactly 12_500 times.
"""


def three_sum_closest(nums: list[int], target: int) -> int:
    s = sorted(nums)
    n = len(s)
    best = s[0] + s[1] + s[2]
    i = 0
    while i < n - 2:
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = s[i] + s[lo] + s[hi]
            if total == target:
                return total
            if abs(total - target) < abs(best - target):
                best = total
            if total < target:
                lo += 1
            else:
                hi -= 1
        i += 1
    return best


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % 2147483648


def build_case(seed: int, count: int) -> list[int]:
    v = []
    state = seed
    for _ in range(count):
        state = lcg_next(state)
        v.append((state % 21) - 10)
    return v


def target_for(idx: int) -> int:
    return (-12, -6, -1, 0, 1, 5, 11, 19)[idx]


def main() -> None:
    m_cases = 8
    n_values = 16
    k_iters = 100_000

    sets = [build_case(m * 1000003 + 12345, n_values) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        total += three_sum_closest(sets[idx], target_for(idx))
    print(total)


if __name__ == "__main__":
    main()
