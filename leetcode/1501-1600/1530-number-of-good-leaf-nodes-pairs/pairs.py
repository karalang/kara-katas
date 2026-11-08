# LeetCode #1530: Number of Good Leaf Nodes Pairs -- mirrors pairs.kara
# (the ★ arm): each node returns how many leaves sit each number of edges
# below it, and counts the pairs across its two sides. O(n d^2).
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def leaves_below(node, distance, pairs):
    counts = [0] * distance
    if node is not None:
        if node.left is None and node.right is None:
            counts[0] = 1
        else:
            l = leaves_below(node.left, distance, pairs)
            r = leaves_below(node.right, distance, pairs)
            for i in range(distance):
                for j in range(distance - i - 1):
                    pairs[0] += l[i] * r[j]
            for i in range(distance - 1):
                counts[i + 1] = l[i] + r[i]
    return counts


def count_pairs(root, distance):
    pairs = [0]
    leaves_below(root, distance, pairs)
    return pairs[0]


def make(at, vals, left, right):
    if at < 0:
        return None
    return TreeNode(vals[at], make(left[at], vals, left, right), make(right[at], vals, left, right))


def from_level_order(tokens):
    vals, place = [], []
    for t in tokens:
        place.append(-1 if t == 0 else len(vals))
        if t != 0:
            vals.append(t)
    left = [-1] * len(vals)
    right = [-1] * len(vals)
    nxt = 1
    for i in range(len(tokens)):
        if place[i] >= 0:
            if nxt < len(tokens):
                left[place[i]] = place[nxt]
            if nxt + 1 < len(tokens):
                right[place[i]] = place[nxt + 1]
            nxt += 2
    return make(0, vals, left, right)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(most):
    n = next_random() % most + 1
    vals, left, right = [], [], []
    for i in range(n):
        vals.append(next_random() % 100 + 1)
        left.append(-1)
        right.append(-1)
        if i > 0:
            at = next_random() % i
            while True:
                if next_random() % 2 == 0:
                    if left[at] < 0:
                        left[at] = i
                        break
                    at = left[at]
                else:
                    if right[at] < 0:
                        right[at] = i
                        break
                    at = right[at]
    return make(0, vals, left, right)


def batch(count, most):
    check = 0
    for _ in range(count):
        root = random_tree(most)
        distance = next_random() % 10 + 1
        check = mix(check, count_pairs(root, distance))
    print(f"{count} trees of 1 to {most} nodes, distance 1 to 10: checksum {check}")


def main():
    global seed
    examples = [
        ([1, 2, 3, 0, 4], 3),
        ([1, 2, 3, 4, 5, 6, 7], 3),
        ([7, 1, 4, 6, 0, 5, 3, 0, 0, 0, 0, 0, 2], 3),
        ([100], 1),
        ([1, 1, 1], 2),
        ([1, 1, 1], 1),
    ]
    for tokens, distance in examples:
        text = ",".join("null" if t == 0 else str(t) for t in tokens)
        print(f"[{text}], distance {distance} -> {count_pairs(from_level_order(tokens), distance)}")
    seed = 1530
    batch(3000, 12)
    batch(300, 1024)


main()
