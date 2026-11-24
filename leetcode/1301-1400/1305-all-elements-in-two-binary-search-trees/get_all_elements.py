# LeetCode #1305: All Elements in Two Binary Search Trees -- the Python
# mirror of the ★ arm (each tree read in order, the two sorted lists
# merged), with the same harness.
import sys
from collections import deque

sys.setrecursionlimit(20000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def in_order(node, out):
    if node is not None:
        in_order(node.left, out)
        out.append(node.val)
        in_order(node.right, out)


def get_all_elements(root1, root2):
    a = []
    b = []
    in_order(root1, a)
    in_order(root2, b)
    out = []
    i = j = 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while i < len(values):
        if not queue:
            break
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def insert(root, v):
    at = root
    while True:
        if v == at.val:
            return
        nxt = at.left if v < at.val else at.right
        if nxt is None:
            if v < at.val:
                at.left = TreeNode(v)
            else:
                at.right = TreeNode(v)
            return
        at = nxt


def random_bst(n, spread):
    if n == 0:
        return None
    root = TreeNode(next_random() % (2 * spread + 1) - spread)
    for _ in range(1, n):
        insert(root, next_random() % (2 * spread + 1) - spread)
    return root


def show(v):
    return ",".join(str(x) for x in v) if v else "-"


def main():
    global seed
    e1 = get_all_elements(from_level([2, 1, 4]), from_level([1, 0, 3]))
    e2 = get_all_elements(from_level([1, None, 8]), from_level([8, 1]))
    e3 = get_all_elements(None, from_level([5, 1, 7]))
    e4 = get_all_elements(None, None)
    rising = TreeNode(0)
    falling = TreeNode(5000)
    at = rising
    down = falling
    for v in range(1, 5000):
        at.right = TreeNode(v)
        at = at.right
        down.left = TreeNode(5000 - 2 * v)
        down = down.left
    chains = get_all_elements(rising, falling)
    chain_check = 0
    for x in chains:
        chain_check = (chain_check * 131 + x + 100000) % 1000000007
    print(f"{show(e1)} {show(e2)} {show(e3)} {show(e4)} {len(chains)}:{chain_check}")
    seed = 1305
    total = 0
    check = 0
    for i in range(2000):
        spread = 10 if i % 3 == 0 else 1000 if i % 3 == 1 else 100000
        n1 = next_random() % 301
        n2 = next_random() % 301
        r1 = random_bst(n1, spread)
        r2 = random_bst(n2, spread)
        got = get_all_elements(r1, r2)
        total += len(got)
        for x in got:
            check = (check * 131 + x + 100000) % 1000000007
    print(f"2000 random pairs: elements total {total}, checksum {check}")


main()
