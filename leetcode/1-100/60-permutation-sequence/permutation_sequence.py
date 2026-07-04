"""LeetCode #60: Permutation Sequence — factorial number system, O(n²).

Mirror of permutation_sequence.kara: same 0-indexed rank kk = k - 1, same
per-position block size (n-1-pos)!, same `digits.pop(idx)` pick-and-shift, and
the same output format (`n={n} k={k} -> {s}` one line per case) so the two files
diff line-for-line.
"""


def get_permutation(n: int, k: int) -> str:
    # factorials: fact[i] = i!  for i in 0..=n.
    fact = [1]
    for i in range(1, n + 1):
        fact.append(fact[i - 1] * i)

    # Available digits, sorted ascending: 1, 2, …, n.
    digits = list(range(1, n + 1))

    kk = k - 1  # 0-indexed rank
    result = ""
    for pos in range(n):
        block = fact[n - 1 - pos]  # (n-1-pos)! permutations per first-digit block
        idx = kk // block          # which remaining digit leads this block
        kk = kk % block            # descend into that block
        digit = digits.pop(idx)    # emit it and drop it from the pool
        result = f"{result}{digit}"
    return result


def report(n: int, k: int) -> None:
    s = get_permutation(n, k)
    print(f"n={n} k={k} -> {s}")


def main() -> None:
    report(3, 3)       # "213"  (LeetCode example 1)
    report(4, 9)       # "2314" (LeetCode example 2)
    report(3, 1)       # "123"  (LeetCode example 3 — first perm)
    report(1, 1)       # "1"    (degenerate single element)
    report(3, 6)       # "321"  (last perm of n=3)
    report(9, 1)       # "123456789" (first perm of n=9)
    report(9, 362880)  # "987654321" (last perm, k = 9!)


if __name__ == "__main__":
    main()
