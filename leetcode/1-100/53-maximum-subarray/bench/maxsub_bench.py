"""Bench mirror of maxsub_bench.kara — Kadane over a batch of LCG-generated arrays,
i64 sink of per-array answers. CPython. See ../README.md § Benchmarks.

CPython is ~1-2 orders of magnitude slower on this tight scalar loop, so it is
excluded from the headline table by default (KARA_BENCH_INCLUDE_PY=1 to include).
"""


def main() -> None:
    m = 1103515245        # glibc LCG multiplier
    inc = 12345           # glibc LCG increment
    modulus = 2147483648  # 2^31
    windows = 120000      # number of simulated input arrays
    w = 1000              # length of each array

    state = 1             # LCG seed
    sink = 0
    for _ in range(windows):
        state = (state * m + inc) % modulus
        v0 = (state % 100) - 50
        best = here = v0
        for _ in range(1, w):
            state = (state * m + inc) % modulus
            v = (state % 100) - 50
            here = here + v if here + v > v else v
            if here > best:
                best = here
        sink += best
    print(sink)


if __name__ == "__main__":
    main()
