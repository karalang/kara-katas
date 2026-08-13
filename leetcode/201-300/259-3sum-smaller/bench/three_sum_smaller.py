"""Benchmark workload for LeetCode #259 — 3Sum Smaller (Python; scale lane)."""


def main():
    n = 4000
    rounds = 26

    base = []
    state = 259259
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        base.append((state // 65536) % 2001 - 1000)
    probe = sorted(base)
    min_sum = probe[0] + probe[1] + probe[2]
    max_sum = probe[n - 1] + probe[n - 2] + probe[n - 3]
    # Kara/C/Rust/Go truncate integer division toward zero; Python's // floors.
    # (min_sum + max_sum) happens to be even for this seed so the two agree, but
    # that is data-dependent luck -- truncate explicitly so a future seed with an
    # odd negative sum cannot diverge silently.
    _t = min_sum + max_sum
    target = -((-_t) // 2) if _t < 0 else _t // 2

    sink = 0
    for _ in range(rounds):
        s = sorted(base)
        count = 0
        for a in range(n - 2):
            lo, hi = a + 1, n - 1
            while lo < hi:
                if s[a] + s[lo] + s[hi] < target:
                    count += hi - lo
                    lo += 1
                else:
                    hi -= 1
        sink = (sink * 31 + count % 1000000007) % 1000000007
    print(sink)


main()
