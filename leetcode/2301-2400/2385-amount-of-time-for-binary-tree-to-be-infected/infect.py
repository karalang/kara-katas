# LeetCode #2385: Amount of Time for Binary Tree to Be Infected -- the
# Python mirror of infect.kara.

import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, start, best):
    if node is None:
        return 0, -1
    lh, ld = walk(node.left, start, best)
    rh, rd = walk(node.right, start, best)
    height = 1 + max(lh, rh)
    if node.val == start:
        best[0] = max(best[0], max(lh, rh))
        return height, 0
    if ld >= 0:
        best[0] = max(best[0], ld + 1 + rh)
        return height, ld + 1
    if rd >= 0:
        best[0] = max(best[0], rd + 1 + lh)
        return height, rd + 1
    return height, -1


def amount_of_time(root, start):
    best = [0]
    walk(root, start, best)
    return best[0]


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


def main():
    global seed
    texts = ["[1,5,3,null,4,10,6,9,2]", "[1]", "[1,2,3]", "[1,2,3]", "[1,2,null,3,null,4]",
             "[1,null,2,null,3,null,4,null,5]", "[1,2,3,null,null,4,null,5,null,6]"]
    starts = [3, 1, 1, 2, 4, 3, 2]
    for i in range(len(texts)):
        print(f"{texts[i]} from {starts[i]} -> {amount_of_time(parse(texts[i]), starts[i])}")
    seed = 2385
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 60 + 1
        tree = random_tree(n)
        minutes = amount_of_time(tree, 1 + next_random() % n)
        total += minutes
        check = (check * 31 + minutes) % 1000000007
    print(f"2000 trees: {total} minutes, checksum {check}")
    big = random_tree(100000)
    root = big.val
    chain = [TreeNode(i + 1) for i in range(2000)]
    for i in range(1, 2000):
        chain[i - 1].left = chain[i]
    print(f"10^5 nodes: {amount_of_time(big, 1)} {amount_of_time(big, root)}; chain: {amount_of_time(chain[0], 1000)}")


if __name__ == "__main__":
    main()
