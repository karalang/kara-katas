"""LeetCode 254 - differential harness. Python oracle.

Mirrors differential.kara exactly: the same exhaustive sweep, the same three
generators, and the same ORDER-INDEPENDENT comparison (hash each combination,
sum the hashes -- addition is commutative, so the digest depends on the multiset
and not on generation order).
"""
import sys


def gen_split(n):
    out = []
    if n < 4:
        return out

    def helper(remaining, start, path):
        i = start
        while i * i <= remaining:
            if remaining % i == 0:
                out.append(path + [i, remaining // i])
                path.append(i)
                helper(remaining // i, i, path)
                path.pop()
            i += 1

    helper(n, 2, [])
    return out


def gen_close(n):
    out = []
    if n < 4:
        return out

    def helper(remaining, start, path):
        i = start
        while i * i <= remaining:
            if remaining % i == 0:
                path.append(i)
                helper(remaining // i, i, path)
                path.pop()
            i += 1
        if path and remaining >= start:
            out.append(path + [remaining])

    helper(n, 2, [])
    return out


def gen_iter(n):
    out = []
    if n < 4:
        return out
    stack = [(n, 2, [])]
    while stack:
        remaining, start, path = stack.pop()
        i = start
        while i * i <= remaining:
            if remaining % i == 0:
                out.append(path + [i, remaining // i])
                stack.append((remaining // i, i, path + [i]))
            i += 1
    return out


def digest_of(combos):
    total = 0
    for c in combos:
        h = 1
        for x in c:
            h = (h * 1000003 + x) % 1000000007
        total = (total + h) % 1000000007
    return total


def main():
    hi = 10000
    mismatches = total_combos = factorable = max_combos = max_at = deepest = digest = 0

    for n in range(2, hi + 1):
        a = gen_split(n)
        b = gen_close(n)
        c = gen_iter(n)

        da = digest_of(a)
        if len(a) != len(b) or len(a) != len(c) or da != digest_of(b) or da != digest_of(c):
            mismatches += 1

        total_combos += len(a)
        if a:
            factorable += 1
        if len(a) > max_combos:
            max_combos = len(a)
            max_at = n
        for combo in a:
            deepest = max(deepest, len(combo))
        digest = (digest * 131 + da) % 1000000007

    print(f"range 2..{hi}")
    print(f"factorable {factorable}")
    print(f"total combinations {total_combos}")
    print(f"max combinations {max_combos} at n={max_at}")
    print(f"deepest combination {deepest}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
