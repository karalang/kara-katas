# Benchmark: LeetCode #951 Flip Equivalent Binary Trees -- the ★ arm,
# both pairings tried, on pairs of trees of 100 nodes, LeetCode's
# largest. Mirrors flip_equiv.kara, .c, .rs and go-seq/.
import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def flip_equiv(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and (
        (flip_equiv(a.left, b.left) and flip_equiv(a.right, b.right))
        or (flip_equiv(a.left, b.right) and flip_equiv(a.right, b.left)))


seed = 951


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        node = TreeNode(v)
        cur = root
        while True:
            if next_random() % 2 == 0:
                if cur.left is not None:
                    cur = cur.left
                else:
                    cur.left = node
                    break
            else:
                if cur.right is not None:
                    cur = cur.right
                else:
                    cur.right = node
                    break
    return root


def flipped_copy(t, rename):
    if t is None:
        return None
    l = flipped_copy(t.left, rename)
    r = flipped_copy(t.right, rename)
    if next_random() % 2 == 0:
        return TreeNode(rename[t.val], l, r)
    return TreeNode(rename[t.val], r, l)


def main():
    sys.setrecursionlimit(10000)
    rounds, count, n = 50000, 20, 100
    firsts = []
    seconds = []
    for c in range(count):
        values = list(range(n))
        for i in range(n):
            j = i + next_random() % (n - i)
            values[i], values[j] = values[j], values[i]
        t = random_tree(values)
        rename = list(range(n))
        if c % 2 == 1:
            a = next_random() % n
            b = next_random() % n
            rename[a] = b
            rename[b] = a
        seconds.append(flipped_copy(t, rename))
        firsts.append(t)
    yes = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            bit = 1 if flip_equiv(firsts[k], seconds[k]) else 0
            yes += bit
            check = (check * 31 + bit + k) % 1000000007
    print(f"{rounds} rounds over {count} pairs of trees of {n} nodes: {yes} flip equivalent, checksum {check}")


main()
