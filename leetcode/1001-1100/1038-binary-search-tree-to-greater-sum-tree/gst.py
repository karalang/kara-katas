# LeetCode #1038: Binary Search Tree to Greater Sum Tree -- mirror of gst.kara
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def add_greater(node, above):
    if node is None:
        return above
    total = add_greater(node.right, above) + node.val
    node.val = total
    return add_greater(node.left, total)


def bst_to_gst(root):
    add_greater(root, 0)
    return root


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(text):
    inner = text[1:-1]
    if inner == "":
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


def insert(root, v):
    node = root
    while True:
        if v < node.val:
            if node.left is not None:
                node = node.left
            else:
                node.left = TreeNode(v)
                return
        else:
            if node.right is not None:
                node = node.right
            else:
                node.right = TreeNode(v)
                return


def random_tree(size):
    pool = list(range(101))
    for i in range(size):
        j = i + next_random() % (101 - i)
        pool[i], pool[j] = pool[j], pool[i]
    root = TreeNode(pool[0])
    for i in range(1, size):
        insert(root, pool[i])
    return written(root)


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    global seed
    cases = [
        "[4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]",
        "[0,null,1]",
        "[5]",
        "[0]",
        "[100]",
        "[1,0,2]",
        "[3,2,4,1]",
        "[0,null,100]",
        "[100,0]",
        "[50,25,75,12,37,62,87,6,18,31,43,56,68,81,93]",
    ]
    for text in cases:
        print(f"{text} -> {written(bst_to_gst(parse(text)))}")
    seed = 1038
    h = 0
    nodes = 0
    for size in range(1, 101):
        for _ in range(3):
            text = random_tree(size)
            out = written(bst_to_gst(parse(text)))
            h = fold(h, out)
            nodes += size
    print(f"300 random trees, {nodes} nodes: checksum {h}")
    rising = TreeNode(0)
    last = rising
    for v in range(1, 100):
        nxt = TreeNode(v)
        last.right = nxt
        last = nxt
    result = bst_to_gst(rising)
    print(f"a rising chain of 100: checksum {fold(0, written(result))}, top {result.val}")
    falling = TreeNode(100)
    last = falling
    for v in range(99, 0, -1):
        nxt = TreeNode(v)
        last.left = nxt
        last = nxt
    result = bst_to_gst(falling)
    print(f"a falling chain of 100: checksum {fold(0, written(result))}, top {result.val}")


main()
