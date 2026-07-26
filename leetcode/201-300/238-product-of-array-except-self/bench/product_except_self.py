"""Benchmark harness for LeetCode #238 — Product of Array Except Self.

Mirrors product_except_self.kara algorithm-for-algorithm. Committed as the
correctness oracle; not a measured lane.

NOTE on `%`: the sink is negative, and Python's `%` FLOORS while Kara, Rust, C
and Go all TRUNCATE toward zero. Using Python's operator directly would produce
a different sink from the other four for the same correct computation, so
`trunc_mod` below reproduces the truncating semantics.
"""

NP = 8
N = 100000
ITERS = 400


def trunc_mod(a, b):
    r = a % b
    if r != 0 and (a < 0) != (b < 0):
        r -= b
    return r


def product_except_self(nums):
    n = len(nums)
    out = []

    prefix = 1
    for i in range(n):
        out.append(prefix)
        prefix *= nums[i]

    suffix = 1
    for j in range(n - 1, -1, -1):
        out[j] *= suffix
        suffix *= nums[j]

    return out


def lcg_vals(seed, n):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(1 - 2 * ((x // 65536) % 2))
    return out


def main():
    arrays = [lcg_vals(j + 1, N) for j in range(NP)]

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        res = product_except_self(arrays[idx])
        for v, val in enumerate(res):
            sink = trunc_mod(sink + (v + 1) * val, 1000000007)
    print(sink)


if __name__ == "__main__":
    main()
