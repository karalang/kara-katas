# LeetCode #1373 bench -- Python: the ★ arm: one walk up from the leaves;
# each subtree reports whether it is a search tree, its smallest and
# largest key, and its sum.
import sys

sys.setrecursionlimit(50000)

INF = 1 << 62


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def summarize(node, best):
    if node is None:
        return True, INF, -INF, 0
    ls, llo, lhi, lsum = summarize(node.left, best)
    rs, rlo, rhi, rsum = summarize(node.right, best)
    key = node.val
    if ls and rs and lhi < key < rlo:
        total = lsum + key + rsum
        best[0] = max(best[0], total)
        return True, min(llo, key), max(rhi, key), total
    return False, 0, 0, 0


def max_sum_bst(root):
    best = [0]
    summarize(root, best)
    return best[0]


seed = 1373


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 4 search trees of 4 * 10^4 nodes, keys from -4 * 10^4 to 4 * 10^4
    # put in one by one, a key already there skipped, built once; then 300
    # rounds, each giving one node of one tree a new key, both drawn from
    # the checksum so far, and finding that tree's largest search tree
    roots = []
    nodes = []
    for _ in range(4):
        root = TreeNode(0)
        every = [root]
        while len(every) < 40000:
            a = next_random()
            key = (a * 32768 + next_random()) % 80001 - 40000
            at = root
            while key != at.val:
                child = at.left if key < at.val else at.right
                if child is None:
                    node = TreeNode(key)
                    if key < at.val:
                        at.left = node
                    else:
                        at.right = node
                    every.append(node)
                    break
                at = child
        roots.append(root)
        nodes.append(every)
    check = 0
    for r in range(300):
        t = check % 4
        nodes[t][(check // 4) % 40000].val = (check // 160000) % 80001 - 40000
        got = max_sum_bst(roots[t])
        check = (check * 31 + got + r) % 1000000007
    print(f"300 rounds over 4 trees of 40000 nodes: checksum {check}")


main()
