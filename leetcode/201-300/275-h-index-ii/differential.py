#!/usr/bin/env python3
"""LeetCode 275 — differential harness. Mirror of differential.kara.

Three solvers plus a definitional oracle over 9,435 arrays — every non-decreasing
sequence of length 0..7 with values 0..7, then 3,000 randomized sorted arrays for
scale. Same generator, same counters, same digest, line-for-line with the Kāra
version so a divergence is a compiler question, not a translation question.
"""

MAX_LEN = 7
MAX_VAL = 7
RANDOM_CASES = 3000


def h_binary(citations):
    n = len(citations)
    lo, hi = 0, n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if citations[mid] >= n - mid:
            hi = mid
        else:
            lo = mid + 1
    return n - lo


def h_scan(citations):
    n = len(citations)
    h = 0
    i = n - 1
    while i >= 0:
        if citations[i] >= h + 1:
            h += 1
        else:
            i = -1
        i -= 1
    return h


def h_bucket(citations):
    n = len(citations)
    buckets = [0] * (n + 1)
    for c in citations:
        buckets[min(c, n)] += 1
    total = 0
    for h in range(n, -1, -1):
        total += buckets[h]
        if total >= h:
            return h
    return 0


def h_is_valid(citations, h):
    """The definition, counted directly. Refutes an answer; never produces one."""
    n = len(citations)
    if h < 0 or h > n:
        return False
    at_least_h = sum(1 for c in citations if c >= h)
    at_least_h1 = sum(1 for c in citations if c >= h + 1)
    if at_least_h < h:
        return False
    if at_least_h1 >= h + 1:
        return False
    return True


def main():
    cases = exhaustive = mismatches = invalid = 0
    h_zero = h_full = over_n = digest = 0

    for k in range(MAX_LEN + 1):
        row = [0] * k
        more = True
        while more:
            a, b, c = h_binary(row), h_scan(row), h_bucket(row)
            if a != b or a != c:
                mismatches += 1
            if not h_is_valid(row, a):
                invalid += 1
            if a == 0:
                h_zero += 1
            if a == k and k > 0:
                h_full += 1
            if any(v > k for v in row):
                over_n += 1
            digest = (digest * 131 + a + k) % 1000000007
            cases += 1
            exhaustive += 1

            if k == 0:
                more = False
            else:
                i = k - 1
                while i >= 0 and row[i] == MAX_VAL:
                    i -= 1
                if i < 0:
                    more = False
                else:
                    row[i] += 1
                    for j in range(i + 1, k):
                        row[j] = row[i]

    seed = 275275
    for _ in range(RANDOM_CASES):
        seed = (seed * 1103515245 + 12345) & 2147483647
        n = 1 + (seed // 256) % 800
        seed = (seed * 1103515245 + 12345) & 2147483647
        step_cap = 1 + (seed // 256) % 5
        arr = []
        cur = 0
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) & 2147483647
            cur += (seed // 256) % step_cap
            arr.append(cur)
        a, b, c = h_binary(arr), h_scan(arr), h_bucket(arr)
        if a != b or a != c:
            mismatches += 1
        if not h_is_valid(arr, a):
            invalid += 1
        if a == 0:
            h_zero += 1
        if a == n:
            h_full += 1
        if arr[n - 1] > n:
            over_n += 1
        digest = (digest * 131 + a + n) % 1000000007
        cases += 1

    print(f"cases {cases}")
    print(f"of which EXHAUSTIVE (every sorted array, len 0..{MAX_LEN}, vals 0..{MAX_VAL}) {exhaustive}")
    print(f"answers at the floor (h = 0) {h_zero}")
    print(f"answers at the ceiling (h = n) {h_full}")
    print(f"arrays with a citation count above n (the bucket clamp) {over_n}")
    print(f"answers refuted by the DEFINITION {invalid}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
