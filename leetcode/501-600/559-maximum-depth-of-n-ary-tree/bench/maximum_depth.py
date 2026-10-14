# Benchmark for #559: Python mirror of the ★ arm (recursion); see
# maximum_depth.kara. A node is (val, children).
import sys

sys.setrecursionlimit(100000)


def depth(node):
    deepest = 0
    for child in node[1]:
        d = depth(child)
        if d > deepest:
            deepest = d
    return deepest + 1


def max_depth(root):
    return 0 if root is None else depth(root)


# ---- benchmark ---------------------------------------------------------------


def build_random(i, vals, kids):
    return (vals[i], [build_random(k, vals, kids) for k in kids[i]])


def main():
    n = 10000
    count = 100
    rounds = 50
    seed = 559

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
            d = max_depth(trees[(rnd * 7 + g) % count])
            total += d
            checksum = (checksum * 31 + d) % 1000000007
    print(f"{count} trees of {n} nodes, {rounds} rounds: depths sum to {total}, checksum {checksum}")


main()
