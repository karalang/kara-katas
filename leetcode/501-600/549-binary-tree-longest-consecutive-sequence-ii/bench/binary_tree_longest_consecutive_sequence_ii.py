# Benchmark for #549: Python mirror of the ★ arm (post-order, two lengths
# a node); see binary_tree_longest_consecutive_sequence_ii.kara.
import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, best):
    rise = 1
    fall = 1
    l = node.left
    if l is not None:
        r1, f1 = walk(l, best)
        if l.val == node.val + 1:
            rise = r1 + 1
        elif l.val == node.val - 1:
            fall = f1 + 1
    r = node.right
    if r is not None:
        r2, f2 = walk(r, best)
        if r.val == node.val + 1:
            rise = max(rise, r2 + 1)
        elif r.val == node.val - 1:
            fall = max(fall, f2 + 1)
    if rise + fall - 1 > best[0]:
        best[0] = rise + fall - 1
    return rise, fall


def longest_consecutive(root):
    best = [0]
    if root is not None:
        walk(root, best)
    return best[0]


seed = 549


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    firsts = []
    for g in range(count):
        spread = 3 + g % 4
        root = TreeNode(next_random() % spread)
        kept = [root]
        for _ in range(1, 30000):
            c = TreeNode(next_random() % spread)
            node = root
            while True:
                if next_random() % 2 == 0:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = c
                        break
                else:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = c
                        break
            if len(kept) < 16:
                kept.append(c)
        firsts.append(kept)
    total = checksum = 0
    for rnd in range(60):
        for g in range(count):
            d = longest_consecutive(firsts[g][(rnd * 7 + g) % 16])
            total += d
            checksum = (checksum * 31 + d) % 1000000007
    print(f"{count} trees, 60 rounds each: lengths {total}, checksum {checksum}")


sys.setrecursionlimit(10000)
main()
