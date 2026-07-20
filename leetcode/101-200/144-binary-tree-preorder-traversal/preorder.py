"""LeetCode 144 — Binary Tree Preorder Traversal (Python mirror / oracle).

Preorder = root, left subtree, right subtree. The tree is acyclic, so the Kāra
version uses ordinary strong Option children (no weak refs).
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build(vals, lc, rc):
    if not vals:
        return None
    nodes = [TreeNode(v) for v in vals]
    for i in range(len(vals)):
        if lc[i] >= 0:
            nodes[i].left = nodes[lc[i]]
        if rc[i] >= 0:
            nodes[i].right = nodes[rc[i]]
    return nodes[0]


def preorder(node, out):
    if node is None:
        return
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)


def run(vals, lc, rc):
    out = []
    preorder(build(vals, lc, rc), out)
    print(" ".join(str(x) for x in out))


def main():
    run([1, 2, 3], [-1, 2, -1], [1, -1, -1])
    run([], [], [])
    run([1, 2, 3, 4, 5, 6], [1, 3, 5, -1, -1, -1], [2, 4, -1, -1, -1, -1])


main()
