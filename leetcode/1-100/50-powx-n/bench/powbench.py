"""Bench mirror of powbench.kara — recursive fast-power, f64-bits sum sink.
CPython. See ../README.md § Benchmarks."""

import struct


def to_bits(x: float) -> int:
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def fast_pow(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    half = fast_pow(x, n // 2)
    return half * half if n % 2 == 0 else half * half * x


def my_pow(x: float, n: int) -> float:
    return 1.0 / fast_pow(x, -n) if n < 0 else fast_pow(x, n)


MASK64 = (1 << 64) - 1


def main() -> None:
    n_iters, k_reps = 400000, 20
    inv2048 = 2.0**-11  # exact
    acc = 0
    for rep in range(k_reps):
        for i in range(n_iters):
            h = ((i + rep * 7919) * 2654435761) & 2047
            x = 1.0 + h * inv2048
            n = ((i + rep) % 129) - 64
            acc = (acc + to_bits(my_pow(x, n))) & MASK64
    print(acc & 0x7FFFFFFFFFFFFFFF)


if __name__ == "__main__":
    main()
