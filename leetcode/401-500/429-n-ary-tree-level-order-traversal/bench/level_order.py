# Benchmark for #429: mirror of level_order.kara (breadth first, a level
# at a time).
import sys

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val, children):
        self.val = val
        self.children = children


def level_order(root):
    levels = []
    level = [root] if root is not None else []
    while level:
        row = []
        nxt = []
        for node in level:
            row.append(node.val)
            nxt.extend(node.children)
        levels.append(row)
        level = nxt
    return levels


seed = 429


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build_random(i, vals, kids):
    return Node(vals[i], [build_random(k, vals, kids) for k in kids[i]])


def main():
    n = 10000
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rows = 0
    checksum = 0
    for _ in range(rounds):
        reach = 10 + step() % 1000
        vals = []
        kids = []
        for i in range(n):
            vals.append(step() % 10001)
            kids.append([])
            if i > 0:
                back = 1 + step() % min(i, reach)
                kids[i - back].append(i)
        levels = level_order(build_random(0, vals, kids))
        rows += len(levels)
        for row in levels:
            checksum = (checksum * 31 + len(row) * 10007 + row[0] + row[-1]) % 1000000007
    print(f"{rounds} rounds of {n} nodes: {rows} levels, checksum {checksum}")


main()
