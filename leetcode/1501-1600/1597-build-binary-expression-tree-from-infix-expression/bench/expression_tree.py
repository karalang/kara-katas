# LeetCode #1597: Build Binary Expression Tree From Infix Expression
# -- the bench in Python, mirroring expression_tree.kara: two stacks, as
# the shunting-yard reads an expression, on 200000 expressions of up to
# 50 digits, all drawn first, each tree folded to a hash.

import sys

sys.setrecursionlimit(10000)


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def precedence(op):
    return 1 if op in "+-" else 2 if op in "*/" else 0


def join(ops, trees):
    op = ops.pop()
    right = trees.pop()
    left = trees.pop()
    trees.append(Node(op, left, right))


def exp_tree(s):
    ops, trees = [], []
    for c in s:
        if c.isdigit():
            trees.append(Node(c))
        elif c == "(":
            ops.append(c)
        elif c == ")":
            while ops[-1] != "(":
                join(ops, trees)
            ops.pop()
        else:
            while ops and precedence(ops[-1]) >= precedence(c):
                join(ops, trees)
            ops.append(c)
    while ops:
        join(ops, trees)
    return trees.pop()


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def expression(operands, seed):
    if operands <= 1 or next_random(seed) % 4 == 0:
        return str(next_random(seed) % 10)
    left = next_random(seed) % (operands - 1) + 1
    op = "+-*/"[next_random(seed) % 4]
    a = expression(left, seed)
    b = expression(operands - left, seed)
    body = f"{a}{op}{b}"
    return f"({body})" if next_random(seed) % 4 == 0 else body


def fold(tree):
    left = fold(tree.left) if tree.left else 7
    right = fold(tree.right) if tree.right else 11
    return (ord(tree.val) * 1000003 + left * 31 + right * 17) % 1000000007


def main():
    seed = [1597]
    texts = []
    for _ in range(200000):
        operands = next_random(seed) % 50 + 1
        texts.append(expression(operands, seed))
    check = 0
    length = 0
    for s in texts:
        length += len(s)
        check = (check * 31 + fold(exp_tree(s))) % 1000000007
    print(f"200000 expressions, {length} characters: checksum {check}")


main()
