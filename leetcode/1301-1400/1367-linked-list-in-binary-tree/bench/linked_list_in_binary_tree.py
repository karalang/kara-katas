# LeetCode #1367 bench -- Python: every tree node tried as the start of
# the list, and from each the list matched down the tree, either child
# carrying the next value.
import sys

sys.setrecursionlimit(20000)


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def matches_from(head, node):
    if head is None:
        return True
    if node is None:
        return False
    return head.val == node.val and (matches_from(head.next, node.left) or matches_from(head.next, node.right))


def is_sub_path(head, root):
    if root is None:
        return False
    return matches_from(head, root) or is_sub_path(head, root.left) or is_sub_path(head, root.right)


seed = 1367


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 trees of 2500 nodes valued 1 or 2, the constraints' most nodes,
    # each node hung on a random empty child place, built once; then 20000
    # rounds, each flipping one node's value and searching that tree for a
    # list of 8 to 15 values, all drawn from the checksum so far
    trees = []
    for _ in range(20):
        root = TreeNode(1 + next_random() % 2)
        nodes = [root]
        places = [(root, True), (root, False)]
        for _ in range(1, 2500):
            k = next_random() % len(places)
            parent, left = places[k]
            places[k] = places[-1]
            places.pop()
            node = TreeNode(1 + next_random() % 2)
            if left:
                parent.left = node
            else:
                parent.right = node
            places.append((node, True))
            places.append((node, False))
            nodes.append(node)
        trees.append(nodes)
    check = 0
    hits = 0
    for r in range(20000):
        nodes = trees[check % 20]
        flipped = nodes[(check // 20) % 2500]
        flipped.val = 3 - flipped.val
        m = 8 + check % 8
        bits = check // 7
        head = None
        for k in range(m):
            head = ListNode(1 + (bits >> k) % 2, head)
        found = is_sub_path(head, nodes[0])
        if found:
            hits += 1
        check = (check * 31 + m * 2 + (1 if found else 0) + r) % 1000000007
    print(f"20000 rounds over 20 trees of 2500 nodes: {hits} found, checksum {check}")


main()
