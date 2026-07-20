"""LeetCode 145 — Binary Tree Postorder Traversal (Python mirror / oracle).

Postorder = left subtree, right subtree, root. The tree is acyclic, so the Kāra
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


def postorder(node, out):
    if node is None:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)


def run(vals, lc, rc):
    out = []
    postorder(build(vals, lc, rc), out)
    print(" ".join(str(x) for x in out))


def main():
    run([1, 2, 3], [-1, 2, -1], [1, -1, -1])
    run([], [], [])
    run([1, 2, 3, 4, 5, 6], [1, 3, 5, -1, -1, -1], [2, 4, -1, -1, -1, -1])


main()
