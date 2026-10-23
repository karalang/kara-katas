# LeetCode #897 bench: the ★ arm (an in-order walk that relinks as it
# goes) on 200,000 search trees of 100 nodes, LeetCode's largest, each
# made by putting in 100 random values from 0 to 1000; each chain is
# walked into a checksum. The same algorithm as increasing_bst.kara.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def increasing_bst(root):
    head = TreeNode(-1)
    tail = [head]

    def relink(node):
        if node is not None:
            relink(node.left)
            node.left = None
            tail[0].right = node
            tail[0] = node
            relink(node.right)

    relink(root)
    return head.right


seed = 897


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    nodes = 0
    check = 0
    for _ in range(200000):
        root = TreeNode(next_random() % 1001)
        for _ in range(1, 100):
            v = next_random() % 1001
            cur = root
            while True:
                if v < cur.val:
                    if cur.left is not None:
                        cur = cur.left
                    else:
                        cur.left = TreeNode(v)
                        break
                else:
                    if cur.right is not None:
                        cur = cur.right
                    else:
                        cur.right = TreeNode(v)
                        break
        cur = increasing_bst(root)
        while cur is not None:
            nodes += 1
            check = (check * 31 + cur.val) % 1000000007
            cur = cur.right
    print(f"200000 trees of 100 nodes: {nodes} in the chains, checksum {check}")


main()
