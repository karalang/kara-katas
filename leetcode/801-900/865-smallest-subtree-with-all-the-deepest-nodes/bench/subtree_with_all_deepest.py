# LeetCode #865: Smallest Subtree with all the Deepest Nodes -- Python
# mirror of the bench program (the ★ arm, one recursive pass).
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtree_with_all_deepest(root):
    return deepest(root)[1]


def deepest(node):
    if node is None:
        return 0, None
    dl, left = deepest(node.left)
    dr, right = deepest(node.right)
    if dl == dr:
        return dl + 1, node
    if dl > dr:
        return dl + 1, left
    return dr + 1, right


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    vals = list(range(n))
    for i in range(1, n):
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
    nodes = []
    for k in range(n):
        node = TreeNode(vals[k])
        if k > 0:
            while True:
                parent = nodes[next_random() % len(nodes)]
                if next_random() % 2 == 0:
                    if parent.left is None:
                        parent.left = node
                        break
                elif parent.right is None:
                    parent.right = node
                    break
        nodes.append(node)
    return nodes[0] if n else None


def main():
    global seed
    n, rounds = 500, 300000
    seed = 865
    root = random_tree(n)
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    leaf = TreeNode(n)
    total = check = 0
    for _ in range(rounds):
        at = nodes[next_random() % n]
        while at.left is not None and at.right is not None:
            at = nodes[next_random() % n]
        on_left = at.left is None
        if on_left:
            at.left = leaf
        else:
            at.right = leaf
        f = subtree_with_all_deepest(root)
        found = f.val if f else -1
        if on_left:
            at.left = None
        else:
            at.right = None
        total += found
        check = (check * 31 + found + 1) % 1000000007
    print(f"{rounds} rounds on {n} nodes: answers sum to {total}, checksum {check}")


main()
