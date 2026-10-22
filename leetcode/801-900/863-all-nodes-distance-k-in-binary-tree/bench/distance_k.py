# LeetCode #863: All Nodes Distance K in Binary Tree -- Python mirror of the
# bench program (the ★ arm, parents, then a breadth-first search).


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def distance_k(root, target, k):
    parent = {}
    start = None
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        if node.val == target:
            start = node
        if node.left:
            parent[node.left.val] = node
            stack.append(node.left)
        if node.right:
            parent[node.right.val] = node
            stack.append(node.right)
    if start is None:
        return []
    seen = {start.val}
    level = [start]
    for _ in range(k):
        nxt = []
        for node in level:
            near = []
            if node.left:
                near.append(node.left)
            if node.right:
                near.append(node.right)
            if node.val in parent:
                near.append(parent[node.val])
            for m in near:
                if m.val not in seen:
                    seen.add(m.val)
                    nxt.append(m)
        level = nxt
    return sorted(node.val for node in level)


seed = 863


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
    n = 500
    queries = 200000
    root = random_tree(n)
    total = 0
    check = 0
    for _ in range(queries):
        target = next_random() % n
        k = next_random() % 20
        found = distance_k(root, target, k)
        total += len(found)
        for v in found:
            check = (check * 31 + v + 1) % 1000000007
    print(f"{queries} queries on {n} nodes: {total} nodes found, checksum {check}")


main()
