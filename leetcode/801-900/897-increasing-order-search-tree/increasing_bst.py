# LeetCode #897: Increasing Order Search Tree -- Python mirror of the
# relinking in-order walk in increasing_bst.kara, with the same test
# harness.
#
# Walk the tree in order, keeping the tail of the chain built so far
# (starting from a placeholder head). Each node reached loses its left
# child and becomes the tail's right child, then the new tail. The
# nodes are reused, and each right subtree is passed on before its node
# is relinked. O(n) time, O(height) stack.

from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# A tree from LeetCode's level order, None for a missing child.
def from_level_order(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


# LeetCode's level order of a tree, "null" for a missing child, with the
# trailing nulls dropped.
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
    return "[" + ", ".join(out) + "]"


def show(vals):
    before = to_level_order(from_level_order(vals))
    print(f"root = {before} -> {to_level_order(increasing_bst(from_level_order(vals)))}")


# A search tree of n distinct values from 0 to 1000, put in at random,
# in increasing order (kind 1) or in decreasing order (kind 2).
def random_bst(n, kind):
    pool = list(range(1001))
    for i in range(n):
        j = i + next_random() % (1001 - i)
        pool[i], pool[j] = pool[j], pool[i]
    vals = pool[:n]
    if kind == 1:
        vals.sort()
    elif kind == 2:
        vals.sort()
        vals.reverse()
    root = TreeNode(vals[0])
    for v in vals[1:]:
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
    return root


# The number of nodes and a checksum of the values and shape in pre-order.
def summary(root):
    if root is None:
        return (0, 7)
    ln, lc = summary(root.left)
    rn, rc = summary(root.right)
    return (1 + ln + rn, (lc * 31 + rc * 17 + root.val + 3) % 1000000007)


def main():
    global seed
    show([5, 3, 6, 2, 4, None, 8, 1, None, None, None, 7, 9])
    show([5, 1, 7])
    show([0])
    show([1, None, 2, None, 3])
    show([3, 2, None, 1])
    show([2, 1, 3])
    show([4, 1, None, None, 3, 2])
    # LeetCode's largest, 100 nodes: put in at random, increasing and
    # decreasing
    seed = 897
    for kind in range(3):
        n, check = summary(increasing_bst(random_bst(100, kind)))
        print(f"100 nodes of kind {kind} -> {n} in the chain, checksum {check}")
    nodes = 0
    total = 0
    for c in range(300):
        size = 1 + next_random() % 100
        n, check = summary(increasing_bst(random_bst(size, c % 4 % 3)))
        nodes += n
        total = (total * 131 + check) % 1000000007
    print(f"300 random trees of 1 to 100 nodes: {nodes} in the chains, checksum {total}")


main()
