"""LeetCode #129: Sum Root to Leaf Numbers — Python oracle.

Each root-to-leaf path spells a number (digits top->bottom); return their sum.
DFS carrying the running value cur*10 + node.val; add at each leaf.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sum_numbers(root):
    def dfs(node, cur):
        if node is None:
            return 0
        cur = cur * 10 + node.val
        if node.left is None and node.right is None:
            return cur
        return dfs(node.left, cur) + dfs(node.right, cur)

    return dfs(root, 0)


def digit(i, seed):
    return ((i * 7 + seed * 3) % 9) + 1     # 1..9, avoid leading-zero fuss


def build_balanced(lo, hi, seed):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(digit(mid, seed))
    node.left = build_balanced(lo, mid - 1, seed)
    node.right = build_balanced(mid + 1, hi, seed)
    return node


def leaf(v):
    return TreeNode(v)


def main():
    MOD = 1000000007
    sink = 0

    # [1,2,3] -> 12 + 13 = 25
    e1 = TreeNode(1, leaf(2), leaf(3))
    sink = (sink * 1000003 + sum_numbers(e1)) % MOD

    # [4,9,0,5,1] -> 495 + 491 + 40 = 1026
    e2 = TreeNode(4, TreeNode(9, leaf(5), leaf(1)), leaf(0))
    sink = (sink * 1000003 + sum_numbers(e2)) % MOD

    # single node
    sink = (sink * 1000003 + sum_numbers(leaf(7))) % MOD

    for t in range(6):
        n = 7 + t * 2
        root = build_balanced(0, n - 1, t + 1)
        sink = (sink * 1000003 + sum_numbers(root)) % MOD

    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
