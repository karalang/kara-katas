"""LeetCode 254 - Factor Combinations. Python oracle.

Mirrors factor_combinations.kara algorithm-for-algorithm: sqrt-bounded
backtracking with a non-decreasing factor rule, emitting the two-factor split at
each divisor before recursing on the cofactor. Output is canonicalised the same
way (each combination already non-decreasing; the list sorted lexicographically)
so all implementations print identically.
"""


def helper(remaining, start, path, out):
    i = start
    while i * i <= remaining:
        if remaining % i == 0:
            out.append(path + [i, remaining // i])
            path.append(i)
            helper(remaining // i, i, path, out)
            path.pop()
        i += 1


def factor_combinations(n):
    out = []
    if n < 4:
        return out
    helper(n, 2, [], out)
    return out


def render(combos):
    combos = sorted(combos)
    return "[" + ",".join("[" + ",".join(str(x) for x in c) + "]" for c in combos) + "]"


def main():
    for n in [1, 2, 12, 32, 37, 1, 16, 24, 36, 100, 96]:
        print(f"{n} -> {render(factor_combinations(n))}")


if __name__ == "__main__":
    main()
