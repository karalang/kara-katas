# LeetCode #2096: Step-By-Step Directions From a Binary Tree Node to
# Another -- Python mirror of the ★ arm's benchmark (directions.kara): the
# same random tree of 100000 nodes and 1000 questions, each answered by the
# same two depth-first searches.
import sys

sys.setrecursionlimit(100000)
seed = 2096


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def way_to(node, target, way):
    if node is None:
        return False
    if node.val == target:
        return True
    way.append("L")
    if way_to(node.left, target, way):
        return True
    way.pop()
    way.append("R")
    if way_to(node.right, target, way):
        return True
    way.pop()
    return False


def get_directions(root, start_value, dest_value):
    a = []
    b = []
    way_to(root, start_value, a)
    way_to(root, dest_value, b)
    common = 0
    while common < len(a) and common < len(b) and a[common] == b[common]:
        common += 1
    return "U" * (len(a) - common) + "".join(b[common:])


def main():
    n = 100000
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = wide_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        at = nodes[wide_random() % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    root = nodes[0]
    steps = 0
    check = 0
    for _ in range(1000):
        s = wide_random() % n + 1
        t = (s + wide_random() % (n - 1)) % n + 1
        way = get_directions(root, s, t)
        steps += len(way)
        for c in way:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"1000 answers: {steps} steps, checksum {check}")


main()
