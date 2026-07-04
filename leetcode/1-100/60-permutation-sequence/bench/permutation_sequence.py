"""Benchmark workload — Permutation Sequence (LeetCode #60), FACTORIAL solver.

Python mirror of bench/permutation_sequence.kara. Same M=9 rotated (n,k) cases,
factorial-number-system generator over a list, position-weighted checksum, and
sink. CPython is ~20-40x slower per iter, so this mirror runs K=50_000 (1/10th
of the compiled mirrors' K=500_000); the README quotes the projected ratio.
"""

NTAB = [9, 8, 9, 7, 8, 9, 6, 7, 9]
KTAB = [362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000]
M = 9


def get_permutation(n: int, k: int) -> list[int]:
    fact = [1]
    for i in range(1, n + 1):
        fact.append(fact[i - 1] * i)
    digits = list(range(1, n + 1))
    kk = k - 1
    result = []
    for pos in range(n):
        block = fact[n - 1 - pos]
        idx = kk // block
        kk %= block
        result.append(digits.pop(idx))
    return result


def checksum(perm: list[int], n: int) -> int:
    s = 0
    for i in range(n):
        s += perm[i] * (i + 1)
    return s


def main() -> None:
    k_iters = 50_000
    total = 0
    for k in range(k_iters):
        idx = k % M
        perm = get_permutation(NTAB[idx], KTAB[idx])
        total += checksum(perm, NTAB[idx])
    print(total)


if __name__ == "__main__":
    main()
