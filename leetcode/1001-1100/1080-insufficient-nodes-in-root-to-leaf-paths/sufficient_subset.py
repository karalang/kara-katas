# LeetCode #1080: Insufficient Nodes in Root to Leaf Paths -- the Python
# mirror of the ★ arm (sufficient_subset.kara): same algorithm, same
# harness, same output.
import sys

sys.setrecursionlimit(20000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def prune(node, need):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return node if node.val >= need else None
    node.left = prune(node.left, need - node.val)
    node.right = prune(node.right, need - node.val)
    if node.left is None and node.right is None:
        return None
    return node


def sufficient_subset(root, limit):
    return prune(root, limit)


seed = 1080


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(text):
    inner = text[1:-1]
    if not inner:
        return None
    items = [None if s == "null" else int(s) for s in inner.split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            child = TreeNode(items[i])
            node.left = child
            queue.append(child)
        i += 1
        if i < len(items):
            if items[i] is not None:
                child = TreeNode(items[i])
                node.right = child
                queue.append(child)
            i += 1
    return root


def written(root):
    out = []
    queue = [root]
    head = 0
    while head < len(queue):
        n = queue[head]
        if n is not None:
            out.append(str(n.val))
            queue.append(n.left)
            queue.append(n.right)
        else:
            out.append("null")
        head += 1
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


def random_tree(size, spread):
    root = TreeNode(next_random() % (2 * spread + 1) - spread)
    nodes = [root]
    for _ in range(1, size):
        child = TreeNode(next_random() % (2 * spread + 1) - spread)
        while True:
            parent = nodes[next_random() % len(nodes)]
            if next_random() % 2 == 0:
                if parent.left is None:
                    parent.left = child
                    break
            elif parent.right is None:
                parent.right = child
                break
        nodes.append(child)
    return written(root)


def random_path_sum(root):
    node = root
    total = node.val
    while True:
        l, r = node.left, node.right
        if l is None and r is None:
            break
        if r is None:
            node = l
        elif l is None:
            node = r
        else:
            node = l if next_random() % 2 == 0 else r
        total += node.val
    return total


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    cases = [
        ("[1,2,3,4,-99,-99,7,8,9,-99,-99,12,13,-99,14]", 1),
        ("[5,4,8,11,null,17,4,7,1,null,null,5,3]", 22),
        ("[1,2,-3,-5,null,4,null]", -1),
        ("[5]", 5),
        ("[5]", 6),
        ("[1,2,3]", 4),
        ("[1,2,3]", 5),
        ("[10,-5,null,-5]", 0),
        ("[10,-5,null,-5]", 1),
        ("[0,1,-1,null,null,2,null]", 1),
    ]
    for text, limit in cases:
        print(f"{text} limit {limit} -> {written(sufficient_subset(parse(text), limit))}")
    h = 0
    kept = 0
    for t in range(300):
        size = t + 1
        text = random_tree(size, 10)
        limit = random_path_sum(parse(text)) + next_random() % 7 - 3
        out = written(sufficient_subset(parse(text), limit))
        if out != "[]":
            kept += 1
        h = fold(h, out)
    print(f"300 random trees: {kept} keep their root, checksum {h}")
    top = TreeNode(1)
    last = top
    for _ in range(1, 5000):
        nxt = TreeNode(1)
        last.left = nxt
        last = nxt
    text = written(top)
    whole = written(sufficient_subset(parse(text), 5000))
    print(f"a chain of 5000 at 5000 -> {len(whole)} characters, same {'true' if whole == text else 'false'}")
    print(f"a chain of 5000 at 5001 -> {written(sufficient_subset(parse(text), 5001))}")


main()
