# LeetCode #1522: Diameter of N-Ary Tree -- mirrors diameter.kara, the ★
# arm: a depth-first walk returns each node's height and keeps the
# longest path through its two highest children.
import sys

sys.setrecursionlimit(100000)


class Node:
    def __init__(self, val, children):
        self.val = val
        self.children = children


def height(node, best):
    first = second = 0
    for child in node.children:
        h = height(child, best) + 1
        if h > first:
            second, first = first, h
        elif h > second:
            second = h
    best[0] = max(best[0], first + second)
    return first


def diameter(root):
    best = [0]
    height(root, best)
    return best[0]


def from_level_order(tokens):
    vals = [tokens[0]]
    kids = [[]]
    parent = 0
    for t in tokens[2:]:
        if t is None:
            parent += 1
        else:
            kids[parent].append(len(vals))
            vals.append(t)
            kids.append([])
    return build(vals, kids)


def build(vals, kids):
    n = len(vals)
    made = [None] * n
    for i in range(n - 1, -1, -1):
        made[i] = Node(vals[i], [made[c] for c in kids[i]])
    return made[0]


seed = 1522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(most, window):
    n = next_random() % most + 1
    vals = []
    kids = [[] for _ in range(n)]
    for i in range(n):
        vals.append(next_random() % 1000)
        if i > 0:
            kids[i - 1 - next_random() % min(i, window)].append(i)
    return build(vals, kids)


def batch(count, most, window):
    check = 0
    for _ in range(count):
        check = mix(check, diameter(random_tree(most, window)))
    print(f"{count} trees of 1 to {most} nodes, parents within {window}: checksum {check}")


examples = [
    [1, None, 3, 2, 4, None, 5, 6],
    [1, None, 2, None, 3, 4, None, 5, None, 6],
    [1, None, 2, 3, 4, 5, None, None, 6, 7, None, 8, None, 9, 10, None, None, 11, None, 12, None, 13, None, None, 14],
    [7],
]
for k, tokens in enumerate(examples):
    print(f"example {k + 1} -> diameter {diameter(from_level_order(tokens))}")
batch(3000, 10, 10)
batch(300, 300, 300)
batch(300, 300, 3)
batch(3, 10000, 30)
