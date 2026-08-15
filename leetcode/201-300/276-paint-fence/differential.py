#!/usr/bin/env python3
"""LeetCode 276 — differential harness. Mirror of differential.kara.

Three solvers over 474 (n, k) pairs — 75 of them checked against brute-force
enumeration of every painting. Same generator, same counters, same digest,
line-for-line with the Kāra version so a divergence is a compiler question.

NOTE ON PYTHON AS THE MIRROR: Python's integers are arbitrary-precision, so it
cannot reproduce the i64 envelope by overflowing. `max_safe_n` below computes the
same bound Kāra's does, by the same pre-multiply guard against the same explicit
limit — the envelope is arithmetic the harness performs, not a property of the
host's integer type. That is what lets the two agree exactly.
"""

I64_MAX = 9223372036854775807


def ways_two_state(n, k):
    if n == 0:
        return 0
    if n == 1:
        return k
    same, diff = k, k * (k - 1)
    for _ in range(3, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff


def ways_recurrence(n, k):
    if n == 0:
        return 0
    if n == 1:
        return k
    prev2, prev1 = k, k * k
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, (prev1 + prev2) * (k - 1)
    return prev1


def ways_brute(n, k):
    if n == 0:
        return 0
    colours = [0] * n
    count = 0
    more = True
    while more:
        ok = True
        for i in range(2, n):
            if colours[i] == colours[i - 1] == colours[i - 2]:
                ok = False
        if ok:
            count += 1
        p = n - 1
        while p >= 0 and colours[p] == k - 1:
            colours[p] = 0
            p -= 1
        if p < 0:
            more = False
        else:
            colours[p] += 1
    return count


def max_safe_n(k):
    if k <= 1:
        return 200
    if k > 3037000499:
        return 1
    prev2, prev1 = k, k * k
    n = 2
    while n < 200:
        if prev1 > I64_MAX - prev2:
            break
        s = prev1 + prev2
        if s > I64_MAX // (k - 1):
            break
        prev2, prev1 = prev1, s * (k - 1)
        n += 1
    return n


def main():
    cases = exhaustive = mismatches = brute_disagreements = 0
    digest = widest_n = envelope_k2 = envelope_k100000 = 0

    for k in range(1, 13):
        n = 1
        size = k
        while n <= 12 and size <= 200000:
            a = ways_two_state(n, k)
            b = ways_recurrence(n, k)
            c = ways_brute(n, k)
            if a != b:
                mismatches += 1
            if a != c:
                brute_disagreements += 1
            digest = (digest * 131 + a) % 1000000007
            cases += 1
            exhaustive += 1
            n += 1
            size *= k
            if k == 1:
                size = 200001

    for kk in [1, 2, 3, 5, 10, 97, 1000, 65536, 100000]:
        cap = max_safe_n(kk)
        if kk == 2:
            envelope_k2 = cap
        if kk == 100000:
            envelope_k100000 = cap
        for n in range(1, cap + 1):
            a = ways_two_state(n, kk)
            b = ways_recurrence(n, kk)
            if a != b:
                mismatches += 1
            if n > widest_n:
                widest_n = n
            digest = (digest * 131 + a) % 1000000007
            cases += 1

    print(f"cases {cases}")
    print(f"of which checked against the DEFINITION (brute force) {exhaustive}")
    print(f"largest n reached, all k (k=1 never grows, so it runs to the walk cap) {widest_n}")
    print(f"envelope at k=2 {envelope_k2}, at k=100000 {envelope_k100000}")
    print(f"brute-force disagreements {brute_disagreements}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
