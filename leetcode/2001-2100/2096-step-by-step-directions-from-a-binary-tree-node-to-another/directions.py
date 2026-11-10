# LeetCode #2096: Step-By-Step Directions From a Binary Tree Node to
# Another -- Python mirror of the ★ arm (directions.kara): the way from the
# root to each node by a depth-first search, the common start dropped, a
# `U` for each step the start has left. The search recurses as deep as the
# tree, so it runs in a thread with a large stack.
import sys
import threading


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def way_to(node, target, way):
    if node is None:
        return False
    if node.val == target:
        return True
    way.append("L")
    if way_to(node.left, target, way):
        return True
    way.pop()
    way.append("R")
    if way_to(node.right, target, way):
        return True
    way.pop()
    return False


def get_directions(root, start_value, dest_value):
    a = []
    b = []
    way_to(root, start_value, a)
    way_to(root, dest_value, b)
    common = 0
    while common < len(a) and common < len(b) and a[common] == b[common]:
        common += 1
    return "U" * (len(a) - common) + "".join(b[common:])


# ---- test harness -----------------------------------------------------------

seed = 2096


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


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
        j = wide_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        at = nodes[wide_random() % k]
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


def main():
    examples = [
        ("[5,1,2,3,null,6,4]", 3, 6),
        ("[2,1]", 2, 1),
        ("[2,1]", 1, 2),
        ("[1,2,3,4,5,6,7]", 4, 5),
        ("[1,2,3,4,5,6,7]", 7, 4),
        ("[1,2,null,3,null,4]", 1, 4),
        ("[1,null,2,null,3,4]", 4, 2),
    ]
    for text, s, t in examples:
        print(f'{text} from {s} to {t} -> "{get_directions(parse(text), s, t)}"')
    steps = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 59 + 2
        root = random_tree(n)
        s = next_random() % n + 1
        t = (s + next_random() % (n - 1)) % n + 1
        way = get_directions(root, s, t)
        steps += len(way)
        for c in way:
            check = (check * 31 + ord(c)) % 1000000007
        check = (check * 31 + 1) % 1000000007
    print(f"2000 trees: {steps} steps, checksum {check}")
    n = 100000
    root = random_tree(n)
    s = wide_random() % n + 1
    t = (s + wide_random() % (n - 1)) % n + 1
    way = get_directions(root, s, t)
    print(f"100000 random nodes: {len(way)} steps, {way.count('U')} up")
    chain = [TreeNode(v) for v in range(1, n + 1)]
    for i in range(1, n):
        chain[i - 1].left = chain[i]
    down = get_directions(chain[0], 1, n)
    up = get_directions(chain[0], n, 2)
    print(f'a chain of 100000: {len(down)} steps down, {len(up)} up, ends "{down[-3:]}" "{up[:3]}"')


sys.setrecursionlimit(1000000)
threading.stack_size(512 * 1024 * 1024)
worker = threading.Thread(target=main)
worker.start()
worker.join()
