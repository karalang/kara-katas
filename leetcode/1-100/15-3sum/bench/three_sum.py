"""Benchmark workload — 3Sum (LeetCode #15).

Python mirror of bench/three_sum.kara. Same LCG generator, sort + two-pointer
dedup, and sink. CPython is multi-second per sample at K=1M, so this mirror
runs K=100_000 (1/10th) and the README quotes the projected ratio. M divides
100_000 evenly, so each of the 8 cases is hit exactly 12_500 times.
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    s = sorted(nums)
    n = len(s)
    result: list[list[int]] = []
    i = 0
    while i < n - 2:
        if i > 0 and s[i] == s[i - 1]:
            i += 1
            continue
        if s[i] > 0:
            break
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = s[i] + s[lo] + s[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([s[i], s[lo], s[hi]])
                lo += 1
                hi -= 1
                while lo < hi and s[lo] == s[lo - 1]:
                    lo += 1
                while lo < hi and s[hi] == s[hi + 1]:
                    hi -= 1
        i += 1
    return result


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % 2147483648


def build_case(seed: int, count: int) -> list[int]:
    v = []
    state = seed
    for _ in range(count):
        state = lcg_next(state)
        v.append((state % 21) - 10)
    return v


def main() -> None:
    m_cases = 8
    n_values = 16
    k_iters = 100_000

    sets = [build_case(m * 1000003 + 12345, n_values) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        r = three_sum(sets[idx])
        total += len(r)
    print(total)


if __name__ == "__main__":
    main()
