# LeetCode #1257 bench, in Python: the ★ arm (each region's parent in a
# dict, the regions holding `region1` in a set, then a walk up from
# `region2` until it meets one of them) on 20 random trees of 10000
# regions built once, each nested broadly or deeply, with 250 random pairs
# asked of each; every region found folded into a checksum.


def find_smallest_region(regions, region1, region2):
    parent = {}
    for lst in regions:
        for child in lst[1:]:
            parent[child] = lst[0]
    holding = {region1}
    at = region1
    while at in parent:
        at = parent[at]
        holding.add(at)
    at = region2
    while at not in holding:
        at = parent[at]
    return at


seed = 1257


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def name(i):
    return f"r{i}"


def random_regions(n, spread):
    children = [[] for _ in range(n)]
    for i in range(1, n):
        lo = max(i - spread, 0)
        children[lo + next_random() % (i - lo)].append(i)
    regions = [[name(p)] + [name(c) for c in children[p]] for p in range(n) if children[p]]
    for i in range(len(regions) - 1, 0, -1):
        j = next_random() % (i + 1)
        regions[i], regions[j] = regions[j], regions[i]
    return regions


def main():
    trees = [random_regions(10000, [3, 30, 1000000, 10][t % 4]) for t in range(20)]
    check = 0
    for regions in trees:
        for _ in range(250):
            x = name(next_random() % 10000)
            y = name(next_random() % 10000)
            for b in find_smallest_region(regions, x, y).encode():
                check = (check * 131 + b) % 1000000007
    print(f"20 trees of 10000 regions, 250 pairs each: checksum {check}")


main()
