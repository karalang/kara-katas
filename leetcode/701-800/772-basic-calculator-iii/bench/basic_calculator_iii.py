# LeetCode 772 — Basic Calculator III: benchmark, the ★ arm in Python.
# Sixty-four random expressions of 2,400 numbers, up to LeetCode's limit
# of 10,000 characters, built once; ROUNDS rounds each evaluate the next.
# At each operator the generator takes the first, from a random start,
# that keeps every value valid: no division by zero, nothing beyond 32
# bits.
import sys

sys.setrecursionlimit(10000)

ROUNDS = 6000
LEAVES = 2400


def trunc_div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


class Cursor:
    def __init__(self, s):
        self.s = s
        self.at = 0

    def peek(self):
        return self.s[self.at] if self.at < len(self.s) else ""

    def sum(self):
        value = self.term()
        while True:
            op = self.peek()
            if op != "+" and op != "-":
                return value
            self.at += 1
            right = self.term()
            value = value + right if op == "+" else value - right

    def term(self):
        value = self.factor()
        while True:
            op = self.peek()
            if op != "*" and op != "/":
                return value
            self.at += 1
            right = self.factor()
            value = value * right if op == "*" else trunc_div(value, right)

    def factor(self):
        if self.peek() == "(":
            self.at += 1
            value = self.sum()
            self.at += 1
            return value
        value = 0
        while self.peek().isdigit():
            value = value * 10 + int(self.peek())
            self.at += 1
        return value


def calculate(s):
    return Cursor(s).sum()


seed = 772


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def combine(a, op, b):
    """The value of a op b, or None if b is 0 under / or it leaves 32 bits."""
    if op == "/" and b == 0:
        return None
    if op == "+":
        v = a + b
    elif op == "-":
        v = a - b
    elif op == "*":
        v = a * b
    else:
        v = trunc_div(a, b)
    return v if -2147483648 <= v <= 2147483647 else None


def build(leaves):
    """A random expression: (text, value, level); the operator at each node
    is the first, from a random start, that keeps the value valid."""
    if leaves == 1:
        if next_random() % 4 == 0:
            n = next_random() % 1000
        else:
            n = next_random() % 10
        return (str(n), n, 3)
    left_leaves = 1 + next_random() % (leaves - 1)
    left = build(left_leaves)
    right = build(leaves - left_leaves)
    k = next_random() % 4
    while combine(left[1], "+-*/"[k], right[1]) is None:
        k = (k + 1) % 4
    op = "+-*/"[k]
    level = 1 if op in "+-" else 2
    if left[2] < level or next_random() % 4 == 0:
        left_text = f"({left[0]})"
    else:
        left_text = left[0]
    if right[2] < level or (right[2] == level and op != "+") or next_random() % 4 == 0:
        right_text = f"({right[0]})"
    else:
        right_text = right[0]
    return (left_text + op + right_text, combine(left[1], op, right[1]), level)


def main():
    pool = [build(LEAVES)[0] for _ in range(64)]
    longest = max(len(s) for s in pool)
    check = 0
    for r in range(ROUNDS):
        value = calculate(pool[r % 64])
        check = ((check * 31 + value) % 1000000007 + 1000000007) % 1000000007
    print(f"{ROUNDS} expressions of up to {longest} characters: checksum {check}")


main()
