# LeetCode #1628: Design an Expression Tree With Evaluate Function -- the
# bench's Python mirror: a Node base class, one class per operator, on
# 20000 random postfix expressions of 50 operands, all drawn first.


def truncate(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


class Node:
    def evaluate(self):
        raise NotImplementedError


class Number(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Binary(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(Binary):
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class Subtract(Binary):
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Multiply(Binary):
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class Divide(Binary):
    def evaluate(self):
        return truncate(self.left.evaluate(), self.right.evaluate())


OPERATORS = {"+": Add, "-": Subtract, "*": Multiply, "/": Divide}


class TreeBuilder:
    def build_tree(self, postfix):
        stack = []
        for token in postfix:
            if token in OPERATORS:
                right = stack.pop()
                left = stack.pop()
                stack.append(OPERATORS[token](left, right))
            else:
                stack.append(Number(int(token)))
        return stack.pop()


def evaluate_postfix(postfix):
    return TreeBuilder().build_tree(postfix).evaluate()


seed = 1628


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def expression(leaves, top, tokens):
    if leaves == 1:
        v = (next_random() * 32768 + next_random()) % top
        tokens.append(str(v))
        return v
    left = next_random() % (leaves - 1) + 1
    a = expression(left, top, tokens)
    b = expression(leaves - left, top, tokens)
    op = ["+", "-", "*", "/"][next_random() % 4]
    if op == "/" and b == 0:
        op = "*"
    if op == "*" and abs(a * b) > 1000000000:
        op = "+"
    if op == "+" and abs(a + b) > 1000000000:
        op = "-"
    if op == "-" and abs(a - b) > 1000000000:
        op = "+"
    tokens.append(op)
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return truncate(a, b)


expressions = []
for _ in range(20000):
    postfix = []
    expression(50, 100001, postfix)
    expressions.append(postfix)
check = 0
total = 0
for postfix in expressions:
    got = evaluate_postfix(postfix)
    total += got
    check = (check * 31 + got + 1) % 1000000007
print(f"20000 expressions of 50 operands: values sum to {total}, checksum {check}")
