#!/usr/bin/env python3
"""LeetCode 277 — differential harness. Mirror of differential.kara.

Same three solvers, same enumeration, same counters, same digest. Checks both
the answer and the question count on every case.
"""


def knows(m, a, b, calls):
    calls[0] += 1
    return m[a][b]


def solve_scan(m, n, calls):
    cand = 0
    for i in range(1, n):
        if knows(m, cand, i, calls):
            cand = i
    for j in range(n):
        if j != cand:
            if knows(m, cand, j, calls):
                return -1
            if not knows(m, j, cand, calls):
                return -1
    return cand


def solve_stack(m, n, calls):
    st = list(range(n))
    while len(st) > 1:
        a = st.pop()
        b = st.pop()
        st.append(b if knows(m, a, b, calls) else a)
    cand = st[0]
    for j in range(n):
        if j != cand:
            if knows(m, cand, j, calls):
                return -1
            if not knows(m, j, cand, calls):
                return -1
    return cand


def solve_brute(m, n, calls):
    for i in range(n):
        ok = True
        for j in range(n):
            if i != j:
                if knows(m, i, j, calls):
                    ok = False
                if not knows(m, j, i, calls):
                    ok = False
        if ok:
            return i
    return -1


def from_mask(n, mask):
    m = []
    bit = 0
    for a in range(n):
        r = []
        for b in range(n):
            if a == b:
                r.append(False)
            else:
                r.append((mask // (2 ** bit)) % 2 == 1)
                bit += 1
        m.append(r)
    return m


def main():
    cases = exhaustive = with_celebrity = 0
    scan_vs_stack = vs_definition = bound_violations = 0
    worst_scan = worst_stack = worst_brute_over = digest = 0

    for n in range(1, 5):
        for mask in range(2 ** (n * n - n)):
            m = from_mask(n, mask)
            c1, c2, c3 = [0], [0], [0]
            a1 = solve_scan(m, n, c1)
            a2 = solve_stack(m, n, c2)
            a3 = solve_brute(m, n, c3)
            if a1 != a2:
                scan_vs_stack += 1
            if a1 != a3 or a2 != a3:
                vs_definition += 1
            if a3 >= 0:
                with_celebrity += 1
            bound = 3 * (n - 1)
            if c1[0] > bound or c2[0] > bound:
                bound_violations += 1
            worst_scan = max(worst_scan, c1[0])
            worst_stack = max(worst_stack, c2[0])
            if c3[0] > bound:
                worst_brute_over = max(worst_brute_over, c3[0] - bound)
            digest = (digest * 131 + (a3 + 2)) % 1000000007
            cases += 1
            exhaustive += 1

    seed = 20260816
    for nn in range(5, 10):
        for t in range(120):
            m = []
            for a in range(nn):
                r = []
                for b in range(nn):
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    r.append(a != b and seed % 2 == 0)
                m.append(r)
            if t % 2 == 0:
                star = t % nn
                for p in range(nn):
                    if p != star:
                        m[star][p] = False
                        m[p][star] = True
            c1, c2, c3 = [0], [0], [0]
            a1 = solve_scan(m, nn, c1)
            a2 = solve_stack(m, nn, c2)
            a3 = solve_brute(m, nn, c3)
            if a1 != a2:
                scan_vs_stack += 1
            if a1 != a3 or a2 != a3:
                vs_definition += 1
            if a3 >= 0:
                with_celebrity += 1
            bound = 3 * (nn - 1)
            if c1[0] > bound or c2[0] > bound:
                bound_violations += 1
            worst_scan = max(worst_scan, c1[0])
            worst_stack = max(worst_stack, c2[0])
            digest = (digest * 131 + (a3 + 2)) % 1000000007
            cases += 1

    print(f"cases {cases}")
    print(f"of which EVERY relation on n<=4 {exhaustive}")
    print(f"cases that actually contain a celebrity {with_celebrity}")
    print(f"worst question count: scan {worst_scan}, stack {worst_stack} (bound at n=9 is 24)")
    print(f"brute force exceeded the bound by up to {worst_brute_over} questions")
    print(f"bound violations by the elimination solvers {bound_violations}")
    print(f"digest {digest}")
    print(f"the two elimination solvers disagreeing with EACH OTHER {scan_vs_stack}")
    print(f"either of them disagreeing with the DEFINITION {vs_definition}")


main()
