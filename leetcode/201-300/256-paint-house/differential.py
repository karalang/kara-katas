"""LeetCode 256 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same four cost families, the same
three solvers, the same digest.
"""
import sys


def make_case(seed):
    state = seed
    out = []
    state = (state * 1103515245 + 12345) & 2147483647
    n = (state // 65536) % 12
    state = (state * 1103515245 + 12345) & 2147483647
    family = (state // 65536) % 4

    for _ in range(n):
        if family == 0:
            vals = []
            for _ in range(3):
                state = (state * 1103515245 + 12345) & 2147483647
                vals.append((state // 65536) % 100)
            out.append(tuple(vals))
        elif family == 1:
            state = (state * 1103515245 + 12345) & 2147483647
            lo = (state // 65536) % 5
            state = (state * 1103515245 + 12345) & 2147483647
            hi1 = (state // 65536) % 50 + 50
            state = (state * 1103515245 + 12345) & 2147483647
            hi2 = (state // 65536) % 50 + 50
            out.append((lo, hi1, hi2))
        elif family == 2:
            vals = []
            for _ in range(3):
                state = (state * 1103515245 + 12345) & 2147483647
                vals.append((state // 65536) % 2)
            out.append(tuple(vals))
        else:
            vals = []
            for _ in range(3):
                state = (state * 1103515245 + 12345) & 2147483647
                vals.append((state // 65536) % 1000 + 999000000)
            out.append(tuple(vals))
    return out


def solve_rolling(costs):
    if not costs:
        return 0
    r, b, g = costs[0]
    for i in range(1, len(costs)):
        n_r = costs[i][0] + min(b, g)
        n_b = costs[i][1] + min(r, g)
        n_g = costs[i][2] + min(r, b)
        r, b, g = n_r, n_b, n_g
    return min(r, b, g)


def solve_table(costs):
    if not costs:
        return 0
    dp = [costs[0]]
    for i in range(1, len(costs)):
        p = dp[i - 1]
        dp.append((costs[i][0] + min(p[1], p[2]),
                   costs[i][1] + min(p[0], p[2]),
                   costs[i][2] + min(p[0], p[1])))
    last = dp[-1]
    return min(last)


def solve_memo(costs):
    n = len(costs)
    if n == 0:
        return 0
    memo = [0] * (n * 3)
    seen = [False] * (n * 3)

    def best(i, c):
        if i == n:
            return 0
        key = i * 3 + c
        if seen[key]:
            return memo[key]
        a, b = (c + 1) % 3, (c + 2) % 3
        total = costs[i][c] + min(best(i + 1, a), best(i + 1, b))
        memo[key] = total
        seen[key] = True
        return total

    return min(best(0, 0), best(0, 1), best(0, 2))


def main():
    cases = 6000
    seed = 256256
    mismatches = total_houses = empty_cases = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        costs = make_case(seed)

        a = solve_rolling(costs)
        b = solve_table(costs)
        d = solve_memo(costs)

        if a != b or a != d:
            mismatches += 1
        total_houses += len(costs)
        if not costs:
            empty_cases += 1
        digest = (digest * 131 + (a % 1000000007)) % 1000000007

    print(f"cases {cases}")
    print(f"houses {total_houses}")
    print(f"empty cases {empty_cases}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    main()
