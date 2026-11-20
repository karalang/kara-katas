# LeetCode #1261: Find Elements in a Contaminated Binary Tree -- Python
# mirror of the ★ arm (the tree recovered from the root down, every value
# kept in a set), with the same harness.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def recover(node, value, values):
    if node:
        node.val = value
        values.add(value)
        recover(node.left, 2 * value + 1, values)
        recover(node.right, 2 * value + 2, values)


class FindElements:
    def __init__(self, root):
        self.values = set()
        recover(root, 0, self.values)

    def find(self, target):
        return target in self.values


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def build(present, at):
    if at not in present:
        return None
    return TreeNode(-1, build(present, 2 * at + 1), build(present, 2 * at + 2))


def random_places(n, rng):
    places = [0]
    present = {0}
    while len(places) < n:
        p = places[rng.next() % len(places)]
        child = 2 * p + 1 + rng.next() % 2
        if child < 2097151 and child not in present:
            present.add(child)
            places.append(child)
    return present


def b(x):
    return "true" if x else "false"


def main():
    one = FindElements(TreeNode(-1, None, TreeNode(-1)))
    print(f"{b(one.find(1))} {b(one.find(2))}")
    two = FindElements(build({0, 1, 2, 3, 4}, 0))
    print(f"{b(two.find(1))} {b(two.find(3))} {b(two.find(5))}")
    three = FindElements(build({0, 2, 5, 11}, 0))
    print(f"{b(three.find(2))} {b(three.find(3))} {b(three.find(4))} {b(three.find(5))}")
    rng = Rng(1261)
    found = 0
    check = 0
    for _ in range(300):
        n = rng.next() % 300 + 1
        present = random_places(n, rng)
        places = sorted(present)
        tree = FindElements(build(present, 0))
        for q in range(100):
            if q % 2 == 0:
                target = places[rng.next() % len(places)] % 1000001
            else:
                target = rng.next() * 32 % 1000001
            if tree.find(target):
                found += 1
                check = (check * 131 + target) % 1000000007
    print(f"30000 targets: {found} found, checksum {check}")
    heap = FindElements(build(set(range(10000)), 0))
    hits = sum(1 for t in range(10001) if heap.find(t))
    zig = {0}
    p = 0
    for level in range(20):
        p = 2 * p + 1 + level % 2
        zig.add(p)
    path = FindElements(build(zig, 0))
    on_path = sum(1 for t in range(1000001) if path.find(t))
    print(f"heap of 10000: {hits} of 0 to 10000, {b(heap.find(10000))}; zigzag: {on_path} up to 10^6, {b(path.find(p))}")


main()
