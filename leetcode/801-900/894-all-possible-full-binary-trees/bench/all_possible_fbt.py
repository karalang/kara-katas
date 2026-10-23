# LeetCode #894 bench: Python mirror of all_possible_fbt.kara (the ★ arm,
# recursion with a memo, the trees sharing their subtrees) asked 1,500 times
# for every full tree of 19 nodes.


class TreeNode:
    __slots__ = ("val", "left", "right")

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


# the tree's preorder code, 1 for a node with children and 0 for a leaf,
# folded into a hash
def code(node, h):
    if node is None:
        return h
    if node.left is None:
        return h * 3 % 1000000007
    return code(node.right, code(node.left, (h * 3 + 1) % 1000000007))


def main():
    trees = 0
    check = 0
    for _ in range(1500):
        all_trees = all_possible_fbt(19)
        trees += len(all_trees)
        for t in all_trees:
            check = (check * 131 + code(t, 1)) % 1000000007
    print(f"1500 calls for 19 nodes: {trees} trees, checksum {check}")


main()
