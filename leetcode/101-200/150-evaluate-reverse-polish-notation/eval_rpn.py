"""LeetCode 150 — Evaluate Reverse Polish Notation (Python mirror / oracle).

Left-to-right scan with an operand stack. A token is an operator iff it is a
single character in {+, -, *, /}; everything else is an integer literal (which
may start with '-'). Division truncates toward zero (Python's `//` floors, so
`int(a / b)` semantics are emulated explicitly to match Kāra's `/`).
"""


def is_op(t):
    return len(t) == 1 and t in "+-*/"


def trunc_div(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q


def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if is_op(t):
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(trunc_div(a, b))
        else:
            stack.append(int(t))
    return stack.pop()


def run(tokens):
    print(eval_rpn(tokens))


def main():
    run(["2", "1", "+", "3", "*"])
    run(["4", "13", "5", "/", "+"])
    run(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"])
    run(["-7", "2", "/"])
    run(["4", "-2", "/"])
    run(["3", "-4", "*"])


main()
