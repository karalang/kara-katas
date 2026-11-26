# LeetCode #1791: Find Center of Star Graph -- the ★ arm in Python: the node
# the first two edges share.


def find_center(edges):
    a, b = edges[0]
    return a if a in edges[1] else b


seed = 1791


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_star(n, center):
    edges = []
    for leaf in range(1, n + 1):
        if leaf == center:
            continue
        if next_random() % 2 == 0:
            edges.append([center, leaf])
        else:
            edges.append([leaf, center])
    for i in range(len(edges) - 1, 0, -1):
        j = next_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return edges


def main():
    print(f"{find_center([[1, 2], [2, 3], [4, 2]])} {find_center([[1, 2], [5, 1], [1, 3], [1, 4]])}")
    print(f"{find_center([[1, 2], [1, 3]])} {find_center([[1, 2], [3, 2]])} {find_center([[3, 1], [2, 3]])} {find_center([[1, 4], [4, 2], [3, 4]])}")
    low = random_star(100000, 1)
    high = random_star(100000, 100000)
    center = 1 + next_random() % 100000
    wide = random_star(100000, center)
    print(f"the most: {find_center(low)} {find_center(high)} {find_center(wide)}")
    check = 0
    for _ in range(3000):
        n = 3 + next_random() % 38
        center = 1 + next_random() % n
        edges = random_star(n, center)
        check = (check * 41 + find_center(edges)) % 1000000007
    print(f"3000 random stars: checksum {check}")


main()
