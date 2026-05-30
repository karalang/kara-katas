"""Benchmark workload — 4Sum (LeetCode #18).

Python mirror of bench/four_sum.kara. Same LCG generator, per-case target
bag, sort + two-fix + two-pointer body with dedup and min/max prunes, and
sink. CPython is multi-second per sample at K=1M, so this mirror runs
K=100_000 (1/10th) and the README quotes the projected ratio. M divides
100_000 evenly, so each of the 8 cases is hit exactly 12_500 times.
"""


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    s = sorted(nums)
    n = len(s)
    result: list[list[int]] = []
    a = 0
    while a < n - 3:
        if a > 0 and s[a] == s[a - 1]:
            a += 1
            continue
        if s[a] + s[a + 1] + s[a + 2] + s[a + 3] > target:
            break
        if s[a] + s[n - 1] + s[n - 2] + s[n - 3] < target:
            a += 1
            continue
        b = a + 1
        while b < n - 2:
            if b > a + 1 and s[b] == s[b - 1]:
                b += 1
                continue
            if s[a] + s[b] + s[b + 1] + s[b + 2] > target:
                break
            if s[a] + s[b] + s[n - 1] + s[n - 2] < target:
                b += 1
                continue
            lo, hi = b + 1, n - 1
            while lo < hi:
                total = s[a] + s[b] + s[lo] + s[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    result.append([s[a], s[b], s[lo], s[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and s[lo] == s[lo - 1]:
                        lo += 1
                    while lo < hi and s[hi] == s[hi + 1]:
                        hi -= 1
            b += 1
        a += 1
    return result


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % 2147483648


def build_case(seed: int, count: int) -> list[int]:
    v: list[int] = []
    state = seed
    for _ in range(count):
        state = lcg_next(state)
        v.append((state % 21) - 10)
    return v


def target_for(idx: int) -> int:
    return (-20, -8, -3, 0, 2, 6, 12, 24)[idx]


def main() -> None:
    m_cases = 8
    n_values = 16
    k_iters = 100_000

    sets = [build_case(m * 1000003 + 12345, n_values) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        total += len(four_sum(sets[idx], target_for(idx)))
    print(total)


if __name__ == "__main__":
    main()
