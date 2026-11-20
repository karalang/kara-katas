# LeetCode #1257: Smallest Common Region -- the Python mirror of
# smallest_common_region.kara: each region's parent in a dict, the regions
# holding `region1` in a set, and a walk up from `region2` until it meets
# one of them.


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


seed = 0


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
    global seed
    world = [["Earth", "North America", "South America"], ["North America", "United States", "Canada"],
             ["United States", "New York", "Boston"], ["Canada", "Ontario", "Quebec"], ["South America", "Brazil"]]
    print(f"{find_smallest_region(world, 'Quebec', 'New York')}, {find_smallest_region(world, 'Canada', 'South America')}")
    seed = 1257
    total = check = 0
    for _ in range(200):
        n = next_random() % 1999 + 2
        spread = [1, 3, 10, 1000000][next_random() % 4]
        regions = random_regions(n, spread)
        for _ in range(20):
            x = name(next_random() % n)
            y = name(next_random() % n)
            found = int(find_smallest_region(regions, x, y)[1:])
            total += found
            check = (check * 131 + found) % 1000000007
    print(f"4000 random pairs: total {total}, checksum {check}")
    chain = random_regions(10000, 1)
    forked = [[name(0), name(1), name(5001)]]
    for i in range(1, 10000):
        if i != 5000 and i != 9999:
            forked.append([name(i), name(i + 1)])
    x = find_smallest_region(chain, "r9999", "r5000")
    y = find_smallest_region(forked, "r5000", "r9999")
    z = find_smallest_region(forked, "r4000", "r3000")
    print(f"10000 regions: chain {x}, two chains {y}, one chain {z}")


main()
