# LeetCode #1123: Lowest Common Ancestor of Deepest Leaves -- Python
# mirror of the ★ arm.
import sys

sys.setrecursionlimit(10000)
seed = 1123


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node):
    if node is None:
        return 0, None
    ld, la = walk(node.left)
    rd, ra = walk(node.right)
    if ld == rd:
        return ld + 1, node
    if ld > rd:
        return ld + 1, la
    return rd + 1, ra


def lca_deepest_leaves(root):
    return walk(root)[1]


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
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items):
            if items[i] is not None:
                node.right = TreeNode(items[i])
                queue.append(node.right)
            i += 1
    return root


def show(root):
    items = []
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is None:
            items.append("null")
        else:
            items.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def size(node):
    return 0 if node is None else 1 + size(node.left) + size(node.right)


def random_tree(count, deep):
    pool = list(range(1001))
    for j in range(len(pool) - 1, 0, -1):
        k = next_random() % (j + 1)
        pool[j], pool[k] = pool[k], pool[j]
    root = TreeNode(pool[0])
    nodes = [root]
    for i in range(1, count):
        c = TreeNode(pool[i])
        while True:
            if deep and next_random() % 2 == 0:
                at = nodes[-1]
            else:
                at = nodes[next_random() % len(nodes)]
            if next_random() % 2 == 0:
                if at.left is None:
                    at.left = c
                    break
            elif at.right is None:
                at.right = c
                break
        nodes.append(c)
    return root


def main():
    cases = ["[3,5,1,6,2,0,8,null,null,7,4]", "[1]", "[0,1,3,null,2]", "[1,2,3]", "[1,2,3,4,null,null,null,5]",
             "[1,2,3,4,5,6,7]", "[1,2,null,3,null,4]", "[1,2,3,null,4,null,null,5,6]"]
    for c in cases:
        print(f"{c} -> {show(lca_deepest_leaves(parse(c)))}")
    nodes = check = 0
    for t in range(2000):
        count = next_random() % 1000 + 1
        root = random_tree(count, t % 2 == 1)
        answer = lca_deepest_leaves(root)
        n = size(answer)
        nodes += n
        check = (check * 31 + answer.val + n) % 1000000007
    print(f"2000 random trees: {nodes} nodes under the answers, checksum {check}")


main()
