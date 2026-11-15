# benchmark's Python mirror of create.kara (LeetCode #2196, the ★ arm): a
# dict of nodes made as named, a set of children.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def node_of(nodes, v):
    n = nodes.get(v)
    if n is not None:
        return n
    n = TreeNode(v)
    nodes[v] = n
    return n


def create_binary_tree(descriptions):
    nodes = {}
    children = set()
    for d in descriptions:
        parent = node_of(nodes, d[0])
        child = node_of(nodes, d[1])
        if d[2] == 1:
            parent.left = child
        else:
            parent.right = child
        children.add(d[1])
    for d in descriptions:
        if d[0] not in children:
            return nodes[d[0]]
    return None


seed = 2196


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def random_descriptions():
    n = 10001
    values = list(range(1, 100001))
    for i in range(n):
        j = i + wide_random() % (100000 - i)
        values[i], values[j] = values[j], values[i]
    free = [(0, 1), (0, 0)]
    descriptions = []
    for k in range(1, n):
        pick = wide_random() % len(free)
        p, side = free[pick]
        free[pick] = free[-1]
        free.pop()
        descriptions.append((values[p], values[k], side))
        free.append((k, 1))
        free.append((k, 0))
    for i in range(len(descriptions) - 1, 0, -1):
        j = wide_random() % (i + 1)
        descriptions[i], descriptions[j] = descriptions[j], descriptions[i]
    return descriptions


def weigh(root):
    stack = [(root, 1)] if root is not None else []
    count = 0
    weight = 0
    while stack:
        n, depth = stack.pop()
        count += 1
        weight += n.val * depth
        if n.left is not None:
            stack.append((n.left, depth + 1))
        if n.right is not None:
            stack.append((n.right, depth + 1))
    return count, weight


def main():
    sets = [random_descriptions() for _ in range(20)]
    check = 0
    for _ in range(50):
        for d in sets:
            count, weight = weigh(create_binary_tree(d))
            check = (check * 31 + count + weight % 1000000007) % 1000000007
    print(f"50 passes over 20 trees: checksum {check}")


main()
