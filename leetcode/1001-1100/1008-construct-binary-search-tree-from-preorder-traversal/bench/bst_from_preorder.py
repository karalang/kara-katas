# LeetCode #1008 bench: the ★ arm (recursion with an upper bound) over 50
# preorders of 100 values, drawn once; each of 4000 rounds builds every
# tree, starting from a different preorder, and folds it into a checksum.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def bst_from_preorder(preorder):
    nxt = [0]

    def build(bound):
        if nxt[0] == len(preorder) or preorder[nxt[0]] >= bound:
            return None
        val = preorder[nxt[0]]
        nxt[0] += 1
        left = build(val)
        right = build(bound)
        return TreeNode(val, left, right)

    return build(1 << 62)


def fold(node, depth):
    if node is None:
        return 0
    return (node.val * depth + fold(node.left, depth + 1) * 3 + fold(node.right, depth + 1) * 7) % 1000000007


seed = 1008


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_preorder(n, most):
    seen = [False] * (most + 1)
    vals, left, right = [], [], []
    while len(vals) < n:
        v = 1 + next_random() % most
        if seen[v]:
            continue
        seen[v] = True
        vals.append(v)
        left.append(-1)
        right.append(-1)
        me = len(vals) - 1
        if me > 0:
            at = 0
            while True:
                if v < vals[at]:
                    if left[at] == -1:
                        left[at] = me
                        break
                    at = left[at]
                else:
                    if right[at] == -1:
                        right[at] = me
                        break
                    at = right[at]
    out, stack = [], [0]
    while stack:
        at = stack.pop()
        out.append(vals[at])
        if right[at] != -1:
            stack.append(right[at])
        if left[at] != -1:
            stack.append(left[at])
    return out


def main():
    count, rounds = 50, 4000
    preorders = [random_preorder(100, 1000) for _ in range(count)]
    check = 0
    for r in range(rounds):
        for k in range(count):
            tree = bst_from_preorder(preorders[(r + k) % count])
            check = (check * 31 + fold(tree, 1)) % 1000000007
    print(f"{rounds} rounds over {count} preorders of 100 values: checksum {check}")


main()
