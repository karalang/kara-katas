"""Benchmark workload for LeetCode #258 — Add Digits (Python; scale lane)."""

MASK64 = (1 << 64) - 1


def to_i64(x):
    x &= MASK64
    return x - (1 << 64) if x >= (1 << 63) else x


def add_digits(num):
    n = num
    while n >= 10:
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        n = s
    return n


def main():
    iters = 10000000
    state = 258258
    sink = 0
    for _ in range(iters):
        state = (state * 1103515245 + 12345) & 2147483647
        shift = (state // 65536) % 33
        # Kara/C/Rust/Go wrap on i64 overflow-free here, but the shift can
        # exceed 63 bits of product; emulate i64 truncation explicitly.
        v = to_i64((state // 8) * (1 << shift)) % 9223372036854775807
        sink = (sink + add_digits(v)) % 1000000007
    print(sink)


main()
