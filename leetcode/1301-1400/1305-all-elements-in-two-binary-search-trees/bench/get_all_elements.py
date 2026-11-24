# LeetCode #1305 bench in Python: the ★ arm (each tree read in order, the
# two sorted lists merged) on the same 20 pairs of search trees and 100
# passes.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


seed = 1305


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def random_bst(n):
    root = TreeNode(next_random() % 200001 - 100000)
    for _ in range(1, n):
        insert(root, next_random() % 200001 - 100000)
    return root


def main():
    firsts = []
    seconds = []
    for _ in range(20):
        firsts.append(random_bst(4900))
        seconds.append(random_bst(4900))
    check = 0
    for pass_no in range(100):
        for p in range(20):
            insert(firsts[p], check % 200001 - 100000)
            got = get_all_elements(firsts[p], seconds[p])
            x = got[check % len(got)]
            check = (check * 31 + x + 100000 + len(got) + pass_no) % 1000000007
    print(f"100 passes over 20 pairs of trees: checksum {check}")


main()
