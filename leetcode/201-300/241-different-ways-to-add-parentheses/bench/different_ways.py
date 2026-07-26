"""Benchmark harness for LeetCode #241 — Different Ways to Add Parentheses.

Mirrors different_ways.kara algorithm-for-algorithm, including the deliberately
unmemoized recursion. Committed as the correctness oracle; not a measured lane.
"""

NP = 6
NOPS = 11
ITERS = 30


def tokenize(expr):
    tok = []
    i = 0
    n = len(expr)
    while i < n:
        b = ord(expr[i])
        if b in (43, 45, 42):
            tok.append(b)
            i += 1
        else:
            v = 0
            while i < n:
                d = ord(expr[i])
                if 48 <= d <= 57:
                    v = v * 10 + (d - 48)
                    i += 1
                else:
                    break
            tok.append(v)
    return tok


def ways(tok, lo, hi):
    res = []
    if lo == hi:
        res.append(tok[lo])
        return res
    k = lo + 1
    while k < hi:
        op = tok[k]
        left = ways(tok, lo, k - 1)
        right = ways(tok, k + 1, hi)
        for l in left:
            for r in right:
                if op == 43:
                    res.append(l + r)
                elif op == 45:
                    res.append(l - r)
                else:
                    res.append(l * r)
        k += 2
    return res


def main():
    ops = ["+", "-", "*"]

    toks = []
    for j in range(NP):
        e = []
        for t in range(NOPS + 1):
            e.append(str((t % 9) + 1))
            if t < NOPS:
                e.append(ops[(t + j) % 3])
        toks.append(tokenize("".join(e)))

    sink = 0
    for it in range(ITERS):
        idx = (it * 5) % NP
        tk = toks[idx]
        for v in ways(tk, 0, len(tk) - 1):
            sink += v
    print(sink)


if __name__ == "__main__":
    main()
