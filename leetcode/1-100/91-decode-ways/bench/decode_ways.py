# LeetCode #91 — Python bench peer for decode_ways.kara. Ergonomic foil
# per BENCH.md; not in the timed sweep by default (10M calls × Python's
# per-call overhead lands many seconds of wall, which would block the
# bench). Set KARA_BENCH_INCLUDE_PY=1 to opt in.

from __future__ import annotations

L = 80
N_ITERS = 10_000_000
MODULUS = 1_000_000_007


def decode_ways(b: bytes) -> int:
    n = len(b)
    if n == 0:
        return 0
    zero = ord('0')
    if b[0] == zero:
        return 0

    prev2 = 1
    prev1 = 1

    for i in range(1, n):
        d1 = b[i] - zero
        d0 = b[i - 1] - zero
        two = d0 * 10 + d1

        cur = 0
        if 1 <= d1 <= 9:
            cur += prev1
        if 10 <= two <= 26:
            cur += prev2

        prev2 = prev1
        prev1 = cur

    return prev1


def main() -> None:
    zero = ord('0')
    buf = bytearray(L)
    for j in range(L):
        d = ((j * 3) % 9) + 1
        buf[j] = zero + d

    s = 0
    for k in range(N_ITERS):
        pos = k % L
        d = ((k * 11) % 9) + 1
        buf[pos] = zero + d
        s = (s + decode_ways(bytes(buf))) % MODULUS
    print(s)


if __name__ == "__main__":
    main()
