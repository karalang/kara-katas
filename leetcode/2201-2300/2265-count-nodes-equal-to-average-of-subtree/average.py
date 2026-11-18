# LeetCode #2265: Count Nodes Equal to Average of Subtree -- Python mirror
# of the ★ arm (average.kara): one post-order walk returning each
# subtree's sum and size, a node counted when its value is their floor
# quotient. Output is byte-identical to average.kara.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def average_of_subtree(root):
    matches = 0

    def sum_and_size(node):
        nonlocal matches
        if node is None:
            return 0, 0
        ls, lc = sum_and_size(node.left)
        rs, rc = sum_and_size(node.right)
        s = ls + rs + node.val
        c = lc + rc + 1
        if s // c == node.val:
            matches += 1
        return s, c

    sum_and_size(root)
    return matches


# ---- test harness ---------------------------------------------------------

seed = 2265


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


def random_tree(n, top):
    nodes = [TreeNode(next_random() % (top + 1)) for _ in range(n)]
    for k in range(1, n):
        at = nodes[next_random() % k]
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
    for text in ["[4,8,5,0,1,null,6]", "[1]", "[1,2]", "[3,3,3,3,3]", "[2,1,4]", "[5,null,4,null,3,null,2]", "[0,0,null,0]"]:
        print(f"{text} -> {average_of_subtree(parse(text))}")
    total = 0
    check = 0
    for t in range(2000):
        n = next_random() % 60 + 1
        count = average_of_subtree(random_tree(n, [1, 3, 10, 1000][t % 4]))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"2000 trees: {total} nodes, checksum {check}")
    rand = average_of_subtree(random_tree(1000, 1000))
    sevens = [TreeNode(7) for _ in range(1000)]
    for i in range(1, 1000):
        sevens[i - 1].left = sevens[i]
    down = [TreeNode(999 - i) for i in range(1000)]
    for i in range(1, 1000):
        down[i - 1].right = down[i]
    answers = [rand, average_of_subtree(sevens[0]), average_of_subtree(down[0])]
    print(f"1000 nodes: [{', '.join(str(a) for a in answers)}]")


main()
