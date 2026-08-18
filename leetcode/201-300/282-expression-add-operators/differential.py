#!/usr/bin/env python3
"""LeetCode 282 — differential harness. Mirror of differential.kara.

Backtracking that carries its last operand, against a full enumeration of all
4^(n-1) operator patterns evaluated with a precedence-aware evaluator. Four
checks per case, three of them over both solvers' output.
"""


def solve_backtrack(num, target):
    out = []

    def search(pos, expr, cur, last):
        if pos == len(num):
            if cur == target:
                out.append(expr)
            return
        for end in range(pos + 1, len(num) + 1):
            if end > pos + 1 and num[pos] == "0":
                return
            piece = num[pos:end]
            n = int(piece)
            if pos == 0:
                search(end, piece, n, n)
            else:
                search(end, expr + "+" + piece, cur + n, n)
                search(end, expr + "-" + piece, cur - n, -n)
                search(end, expr + "*" + piece, cur - last + last * n, last * n)

    if len(num) == 0:
        return out
    search(0, "", 0, 0)
    return out


def eval_expr(expr):
    vals, ops = [], []
    cur = 0
    for c in expr:
        if c.isdigit():
            cur = cur * 10 + int(c)
        else:
            vals.append(cur)
            cur = 0
            ops.append({"+": 0, "-": 1, "*": 2}[c])
    vals.append(cur)
    v2, o2 = [vals[0]], []
    for k, op in enumerate(ops):
        if op == 2:
            v2[-1] = v2[-1] * vals[k + 1]
        else:
            o2.append(op)
            v2.append(vals[k + 1])
    acc = v2[0]
    for m, op in enumerate(o2):
        acc = acc + v2[m + 1] if op == 0 else acc - v2[m + 1]
    return acc


def operands_legal(expr):
    start = 0
    for i in range(len(expr) + 1):
        if i == len(expr) or expr[i] in "+-*":
            if i - start > 1 and expr[start] == "0":
                return False
            start = i + 1
    return True


def solve_enumerate(num, target):
    out = []
    n = len(num)
    if n == 0:
        return out
    gaps = n - 1
    for mask in range(4 ** gaps):
        expr = num[0]
        m = mask
        for g in range(gaps):
            choice = m % 4
            m //= 4
            expr += {0: "", 1: "+", 2: "-", 3: "*"}[choice] + num[g + 1]
        if operands_legal(expr) and eval_expr(expr) == target:
            out.append(expr)
    return out


def strip_operators(expr):
    return "".join(c for c in expr if c.isdigit())


def main():
    cases = set_mismatches = wrong_value = illegal_operand = 0
    digits_not_preserved = expressions_found = cases_with_a_solution = digest = 0

    for ln in range(1, 4):
        for code in range(4 ** ln):
            num = ""
            m = code
            for _ in range(ln):
                num += "0123"[m % 4]
                m //= 4
            for target in range(-4, 9):
                a = sorted(solve_backtrack(num, target))
                b = sorted(solve_enumerate(num, target))
                if a != b:
                    set_mismatches += 1
                for x in a:
                    if eval_expr(x) != target:
                        wrong_value += 1
                    if not operands_legal(x):
                        illegal_operand += 1
                    if strip_operators(x) != num:
                        digits_not_preserved += 1
                    digest = (digest * 131 + len(x) + target + 5) % 1000000007
                for x in b:
                    if eval_expr(x) != target:
                        wrong_value += 1
                    if not operands_legal(x):
                        illegal_operand += 1
                    if strip_operators(x) != num:
                        digits_not_preserved += 1
                expressions_found += len(a)
                if a:
                    cases_with_a_solution += 1
                cases += 1

    print(f"cases {cases}, of which have at least one solution {cases_with_a_solution}")
    print(f"expressions returned {expressions_found}")
    print(f"digest {digest}")
    print(f"expressions whose value is wrong {wrong_value}")
    print(f"expressions with an illegal leading zero {illegal_operand}")
    print(f"expressions not preserving the input digits {digits_not_preserved}")
    print(f"set mismatches between the two solvers {set_mismatches}")


main()
