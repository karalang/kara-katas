"""Benchmark workload for LeetCode #150 — Evaluate Reverse Polish Notation (Python; scale lane)."""


def eval_rpn(tok, stk, modp):
    t = len(tok)
    sp = 0
    for i in range(t):
        x = tok[i]
        if x >= 0:
            stk[sp] = x
            sp += 1
        else:
            op = -x - 1
            sp -= 1
            b = stk[sp]
            sp -= 1
            a = stk[sp]
            if op == 0:
                r = a + b
            elif op == 1:
                r = a - b
            elif op == 2:
                r = a * b
            else:
                # Truncate toward zero (a >= 0, b >= 1 here), matching C/Rust/Go/Kāra.
                r = a // b
            r = ((r % modp) + modp) % modp
            stk[sp] = r
            sp += 1
    return stk[0]


def main():
    m = 100000
    punches = 700
    modp = 1000000007
    opr = 1000

    tok = []
    state = 12345

    state = (state * 1103515245 + 12345) & 2147483647
    tok.append(state % opr + 1)
    state = (state * 1103515245 + 12345) & 2147483647
    tok.append(state % opr + 1)
    state = (state * 1103515245 + 12345) & 2147483647
    tok.append(-(state % 4) - 1)

    k = 2
    while k <= m:
        state = (state * 1103515245 + 12345) & 2147483647
        tok.append(state % opr + 1)
        state = (state * 1103515245 + 12345) & 2147483647
        tok.append(-(state % 4) - 1)
        k += 1

    stk = [0, 0, 0, 0]

    sink = 0
    for _pn in range(punches):
        state = (state * 1103515245 + 12345) & 2147483647
        r = state % (m + 1)
        tokpos = 0 if r == 0 else 2 * r - 1
        state = (state * 1103515245 + 12345) & 2147483647
        tok[tokpos] = state % opr + 1
        res = eval_rpn(tok, stk, modp)
        sink = (sink + res) % modp
    print(sink)


main()
