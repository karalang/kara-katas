# LeetCode #2458: Height of Binary Tree After Subtree Removal Queries --
# the Python mirror of heights.kara: every subtree's height, then a walk
# down carrying the height the tree keeps without each node.

import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def height(node, heights):
    if node is None:
        return -1
    h = 1 + max(height(node.left, heights), height(node.right, heights))
    heights[node.val] = h
    return h


def of(node, heights):
    return -1 if node is None else heights[node.val]


def walk(node, depth, rest, heights, answers):
    if node is not None:
        answers[node.val] = rest
        walk(node.left, depth + 1, max(rest, depth + 1 + of(node.right, heights)), heights, answers)
        walk(node.right, depth + 1, max(rest, depth + 1 + of(node.left, heights)), heights, answers)


def tree_queries(root, queries):
    heights = {}
    height(root, heights)
    answers = {}
    walk(root, 0, 0, heights, answers)
    return [answers[q] for q in queries]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(text):
    items = [None if s == "null" else int(s) for s in text[1:-1].split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items):
            if items[i] is not None:
                node.right = TreeNode(items[i])
                queue.append(node.right)
            i += 1
    return root


def random_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        high = next_random()
        at = nodes[(high * 32768 + next_random()) % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    return nodes[0]


def fold(values):
    check = 0
    for v in values:
        check = (check * 31 + v + 1) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    global seed
    texts = ["[1,3,4,2,null,6,5,null,null,null,null,null,7]", "[5,8,9,2,1,3,7,4,6]", "[1,2,3]", "[1,2,null,3,null,4]", "[1,null,2,null,3,null,4,null,5]", "[1,2,3,4,null,null,5,6,null,null,null,7]"]
    asked = [[4], [3, 2, 4, 8], [2, 3], [2, 3, 4], [2, 5], [2, 4, 6, 7, 3, 5]]
    for i in range(len(texts)):
        print(f"{texts[i]} {show(asked[i])} -> {show(tree_queries(parse(texts[i]), asked[i]))}")
    seed = 2458
    check = 0
    for _ in range(2000):
        n = next_random() % 59 + 2
        tree = random_tree(n)
        queries = [v for v in range(1, n + 1) if v != tree.val]
        check = (check * 31 + fold(tree_queries(tree, queries))) % 1000000007
    print(f"2000 trees, every node asked: checksum {check}")
    big = random_tree(2000)
    queries = []
    while len(queries) < 2000:
        q = 1 + next_random() % 2000
        if q != big.val:
            queries.append(q)
    print(f"2000 nodes, 2000 queries: checksum {fold(tree_queries(big, queries))}")
    chain = [TreeNode(i + 1) for i in range(2000)]
    for i in range(1, 2000):
        chain[i - 1].left = chain[i]
    cuts = [2 + next_random() % 1999 for _ in range(2000)]
    print(f"chain of 2000, 2000 queries: checksum {fold(tree_queries(chain[0], cuts))}")


main()
