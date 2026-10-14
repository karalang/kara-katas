# Benchmark for #589: Python mirror of the ★ arm (recursion); see
# preorder.kara. A node is (val, children), and each call returns a
# fresh list.
import sys

sys.setrecursionlimit(100000)


def walk(node, out):
    out.append(node[0])
    for child in node[1]:
        walk(child, out)


def preorder(root):
    out = []
    if root is not None:
        walk(root, out)
    return out


# ---- benchmark ---------------------------------------------------------------


def build_random(i, vals, kids):
    return (vals[i], [build_random(k, vals, kids) for k in kids[i]])


def main():
    n = 10000
    count = 100
    rounds = 30
    seed = 589

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    trees = []
    for _ in range(count):
        reach = 2 + step() % 1000
        vals = []
        kids = []
        for i in range(n):
            vals.append(step() % 10001)
            kids.append([])
            if i > 0:
                back = 1 + step() % min(i, reach)
                kids[i - back].append(i)
        trees.append(build_random(0, vals, kids))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = preorder(trees[(rnd * 7 + g) % count])
            total += len(got)
            for v in got:
                checksum = (checksum * 31 + v) % 1000000007
    print(f"{count} trees of {n} nodes, {rounds} rounds: {total} values listed, checksum {checksum}")


main()
