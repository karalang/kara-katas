# LeetCode 772 — Basic Calculator III: the ★ arm and harness in Python.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}" -> {calculate(s)}')


def random_piece(leaves):
    if leaves == 1:
        if next_random() % 4 == 0:
            n = next_random() % 1000
        else:
            n = next_random() % 10
        return (str(n), n, 3, True)
    left_leaves = 1 + next_random() % (leaves - 1)
    left = random_piece(left_leaves)
    right = random_piece(leaves - left_leaves)
    op = "+-*/"[next_random() % 4]
    level = 1 if op in "+-" else 2
    if left[2] < level or next_random() % 4 == 0:
        left_text = f"({left[0]})"
    else:
        left_text = left[0]
    if right[2] < level or (right[2] == level and op != "+") or next_random() % 4 == 0:
        right_text = f"({right[0]})"
    else:
        right_text = right[0]
    valid = left[3] and right[3]
    value = 0
    if op == "+":
        value = left[1] + right[1]
    elif op == "-":
        value = left[1] - right[1]
    elif op == "*":
        value = left[1] * right[1]
    elif right[1] == 0:
        valid = False
    else:
        value = trunc_div(left[1], right[1])
    if value < -2147483648 or value > 2147483647:
        valid = False
    return (left_text + op + right_text, value, level, valid)


def main():
    global seed
    for s in ["1+1", "6-4/2", "2*(5+5*2)/3+(6/2+8)", "0", "1-1-1", "8/3/2",
              "(1-8)/2", "2147483647", "((((7))))", "1*2-3/4+5*6-7*8+9/10",
              "2-(5-8)", "(0-7)*(0-6)/(2-9)"]:
        show(s)
    seed = 772
    count = 0
    length = 0
    check = 0
    while count < 300:
        piece = random_piece(1 + next_random() % 12)
        if not piece[3]:
            continue
        value = calculate(piece[0])
        count += 1
        length += len(piece[0])
        check = ((check * 31 + value) % 1000000007 + 1000000007) % 1000000007
    print(f"300 random expressions, {length} characters: checksum {check}")


main()
