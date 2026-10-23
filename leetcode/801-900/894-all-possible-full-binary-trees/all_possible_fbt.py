# LeetCode #894: All Possible Full Binary Trees -- Python mirror of the
# memoized recursion in all_possible_fbt.kara, with the same test harness.
#
# A full tree of n nodes is a root over a full left subtree of some odd
# size l and a full right subtree of n - 1 - l. So the trees of n nodes
# are a root over every pair of a tree of l nodes and a tree of n - 1 - l,
# for each odd l. Each size is built once and kept, and the trees share
# those subtrees, as LeetCode's answers do. An even n has none.

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def all_possible_fbt(n):
    memo = {}

    def build(n):
        if n in memo:
            return list(memo[n])
        out = []
        if n == 1:
            out.append(TreeNode(0))
        elif n % 2 == 1:
            left = 1
            while left < n - 1:
                lefts = build(left)
                rights = build(n - 1 - left)
                for l in lefts:
                    for r in rights:
                        out.append(TreeNode(0, l, r))
                left += 2
        memo[n] = list(out)
        return out

    return build(n)


# ---- test harness ----------------------------------------------------------


def to_level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append("null")
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


# the trees in level order, sorted: LeetCode takes them in any order
def sorted_trees(n):
    return sorted(to_level_order(t) for t in all_possible_fbt(n))


def main():
    for n in [7, 3, 1, 2, 5]:
        print(f"n = {n} -> [{', '.join(sorted_trees(n))}]")
    # every n up to 20, LeetCode's largest
    counts = []
    total = 0
    check = 0
    for n in range(1, 21):
        texts = sorted_trees(n)
        counts.append(len(texts))
        total += len(texts)
        for t in texts:
            for b in t.encode():
                check = (check * 131 + b) % 1000000007
    print(f"trees of 1 to 20 nodes: [{', '.join(map(str, counts))}]")
    print(f"{total} trees in all, checksum {check}")


main()
