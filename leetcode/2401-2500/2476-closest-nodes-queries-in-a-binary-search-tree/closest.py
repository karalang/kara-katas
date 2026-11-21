# LeetCode #2476: Closest Nodes Queries in a Binary Search Tree -- the
# Python mirror of closest.kara: an in-order walk reads the values
# ascending, and a bisection by hand finds the first value at least each
# query.

import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, values):
    if node is not None:
        walk(node.left, values)
        values.append(node.val)
        walk(node.right, values)


def closest_nodes(root, queries):
    values = []
    walk(root, values)
    answers = []
    for q in queries:
        lo, hi = 0, len(values)
        while lo < hi:
            mid = (lo + hi) // 2
            if values[mid] < q:
                lo = mid + 1
            else:
                hi = mid
        ceiling = values[lo] if lo < len(values) else -1
        if lo < len(values) and values[lo] == q:
            floor = q
        elif lo > 0:
            floor = values[lo - 1]
        else:
            floor = -1
        answers.append([floor, ceiling])
    return answers


# ---- test harness ---------------------------------------------------------

seed = 2476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


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


def search_tree(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        at = root
        while True:
            if v < at.val:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = TreeNode(v)
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = TreeNode(v)
                    break
    return root


def distinct_values(n, top):
    used = set()
    values = []
    while len(values) < n:
        v = 1 + wide_random() % top
        if v not in used:
            used.add(v)
            values.append(v)
    return values


def fold(answers):
    check = len(answers)
    for a, b in answers:
        check = (check * 31 + a + 1) % 1000000007
        check = (check * 31 + b + 1) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    examples = [
        ("[6,2,13,1,4,9,15,null,null,null,null,null,null,14]", [2, 5, 16]),
        ("[4,null,9]", [3]),
        ("[10,null,20]", [1, 10, 15, 20, 25]),
        ("[5,4,null,3,null,2]", [1, 2, 3, 4, 5, 6]),
    ]
    for text, queries in examples:
        print(f"{text}, {show(queries)} -> {show(closest_nodes(parse(text), queries))}")
    big = search_tree(distinct_values(100000, 1000000))
    asked = [1 + wide_random() % 1000000 for _ in range(10000)]
    print(f"10^5 nodes, 10^4 queries: checksum {fold(closest_nodes(big, asked))}")
    path = search_tree([500 * i for i in range(1, 2001)])
    along = [1 + wide_random() % 1000000 for _ in range(10000)]
    print(f"a path of 2000, 10^4 queries: checksum {fold(closest_nodes(path, along))}")
    check = 0
    for _ in range(2000):
        n = 2 + next_random() % 39
        root = search_tree(distinct_values(n, 60))
        q = 1 + next_random() % 10
        queries = [1 + next_random() % 61 for _ in range(q)]
        check = (check * 31 + fold(closest_nodes(root, queries))) % 1000000007
    print(f"2000 random: checksum {check}")


main()
