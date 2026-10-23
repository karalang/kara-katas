# LeetCode #919: Complete Binary Tree Inserter -- bench: a queue of the
# nodes with a free child slot. Mirrors cbt_inserter.kara.
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class CBTInserter:
    def __init__(self, root):
        self.root = root
        self.open = deque()
        walk = deque([root])
        while walk:
            node = walk.popleft()
            if node.left:
                walk.append(node.left)
            if node.right:
                walk.append(node.right)
            if node.left is None or node.right is None:
                self.open.append(node)

    def insert(self, val):
        child = TreeNode(val)
        parent = self.open[0]
        if parent.left is None:
            parent.left = child
        else:
            parent.right = child
            self.open.popleft()
        self.open.append(child)
        return parent.val

    def get_root(self):
        return self.root


seed = 919


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# A complete tree holding vals in level order.
def complete_tree(vals):
    nodes = [TreeNode(v) for v in vals]
    for i in range(1, len(nodes)):
        parent = nodes[(i - 1) // 2]
        if i % 2 == 1:
            parent.left = nodes[i]
        else:
            parent.right = nodes[i]
    return nodes[0]


def main():
    rounds, n, m = 200, 1000, 50000
    total = 0
    check = 0
    for _ in range(rounds):
        # a fresh tree of n values, then m inserts into it
        vals = [next_random() % 100000 for _ in range(n)]
        inserter = CBTInserter(complete_tree(vals))
        parents = 0
        for _ in range(m):
            parents += inserter.insert(next_random() % 100000)
        root = inserter.get_root()
        total += parents
        check = (check * 1000003 + parents + root.val) % 1000000007
    print(f"{rounds} rounds of {m} inserts into trees of {n}: parents summing to {total}, checksum {check}")


main()
