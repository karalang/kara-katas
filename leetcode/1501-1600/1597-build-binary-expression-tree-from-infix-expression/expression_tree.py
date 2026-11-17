# LeetCode #1597: Build Binary Expression Tree From Infix Expression
# -- mirrors expression_tree.kara: two stacks, as the shunting-yard reads
# an expression.


class Node:
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
    return trees.pop() if trees else None


def serialize(root):
    queue = [root]
    out = []
    at = 0
    while at < len(queue):
        n = queue[at]
        if n is None:
            out.append("null")
        else:
            out.append(n.val)
            queue.append(n.left)
            queue.append(n.right)
        at += 1
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


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


def batch(count, most, seed):
    check = 0
    nodes = 0
    for _ in range(count):
        s = expression(next_random(seed) % most + 1, seed)
        shown = serialize(exp_tree(s))
        for c in shown:
            check = (check * 31 + ord(c) + 1) % 1000000007
        nodes += sum(1 for c in shown if c.isdigit() or c in "+-*/")
    print(f"{count} expressions of up to {most} digits: {nodes} nodes, checksum {check}")


def main():
    for s in ["3*4-2*5", "2-3/(5*2)+1", "1+2+3+4+5", "1", "(((7)))", "9-(8-(7-6))", "1*2+3*4/5-6"]:
        print(f'"{s}" -> {serialize(exp_tree(s))}')
    seed = [1597]
    batch(3000, 4, seed)
    batch(300, 12, seed)
    batch(30, 25, seed)


main()
