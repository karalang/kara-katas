# LeetCode #1791: Find Center of Star Graph -- the bench in Python, mirroring
# find_center.kara: the node the first two edges share.


def find_center(edges):
    a, b = edges[0]
    return a if a == edges[1][0] or a == edges[1][1] else b


seed = 1791


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    stars = []
    for _ in range(2000):
        center = 1 + next_random() % 100
        edges = []
        for leaf in range(1, 101):
            if leaf == center:
                continue
            if next_random() % 2 == 0:
                edges.append([center, leaf])
            else:
                edges.append([leaf, center])
        for i in range(len(edges) - 1, 0, -1):
            j = next_random() % (i + 1)
            edges[i], edges[j] = edges[j], edges[i]
        stars.append(edges)
    check = 0
    for call in range(20000000):
        edges = stars[(check + call) % 2000]
        check = (check * 41 + find_center(edges)) % 1000000007
    print(f"20000000 calls over 2000 stars: checksum {check}")


main()
