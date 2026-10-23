# LeetCode #919: Complete Binary Tree Inserter -- Python mirror of the queue
# of nodes with a free child slot in cbt_inserter.kara, with its harness.
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


def complete_tree(vals):
    nodes = [TreeNode(v) for v in vals]
    for i in range(1, len(nodes)):
        parent = nodes[(i - 1) // 2]
        if i % 2 == 1:
            parent.left = nodes[i]
        else:
            parent.right = nodes[i]
    return nodes[0]


def level_order(root):
    vals = []
    queue = deque([root])
    gap = False
    complete = True
    while queue:
        node = queue.popleft()
        if node is not None:
            if gap:
                complete = False
            vals.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            gap = True
    return vals, complete


def show(vals):
    return "[" + ",".join(str(v) for v in vals) + "]"


def flag(b):
    return "true" if b else "false"


def run(start, inserts):
    c = CBTInserter(complete_tree(start))
    parents = [c.insert(v) for v in inserts]
    vals, complete = level_order(c.get_root())
    print(f"{show(start)} + {show(inserts)}: parents {show(parents)}, tree {show(vals)}, complete {flag(complete)}")


def fold(check, vals):
    h = check
    for v in vals:
        h = (h * 1000003 + v) % 1000000007
    return h


def main():
    run([1, 2], [3, 4])
    run([1], [2, 3, 4, 5, 6, 7, 8])
    run([1, 2, 3], [4])
    run([1, 2, 3, 4, 5, 6], [7, 8])
    run([1, 2, 3, 4, 5, 6, 7], [8, 9, 10])
    run([0, 0, 0], [0, 5000])
    total = 0
    check = 0
    all_complete = True
    for _ in range(200):
        n = 1 + next_random() % 1000
        start = [next_random() % 5001 for _ in range(n)]
        c = CBTInserter(complete_tree(start))
        k = next_random() % 1001
        for _ in range(k):
            p = c.insert(next_random() % 5001)
            total += p
            check = (check * 1000003 + p) % 1000000007
        vals, complete = level_order(c.get_root())
        all_complete = all_complete and complete and len(vals) == n + k
        check = fold(check, vals)
    print(f"200 trees: parents summing to {total}, checksum {check}, all complete {flag(all_complete)}")
    c = CBTInserter(complete_tree([i % 5001 for i in range(1000)]))
    total = 0
    for i in range(10000):
        total += c.insert((7 * i) % 5001)
    vals, complete = level_order(c.get_root())
    print(f"1000 nodes and 10000 inserts: parents summing to {total}, {len(vals)} nodes, checksum {fold(0, vals)}, complete {flag(complete)}")


main()
