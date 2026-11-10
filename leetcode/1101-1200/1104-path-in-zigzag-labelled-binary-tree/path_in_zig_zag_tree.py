# LeetCode #1104: Path In Zigzag Labelled Binary Tree -- Python mirror of
# the ★ arm: walking up from the label, each parent half the label's
# mirror in its row. Same cases and output as path_in_zig_zag_tree.kara.


def path_in_zig_zag_tree(label):
    depth = 1
    while (1 << depth) <= label:
        depth += 1
    path = []
    node = label
    while depth > 0:
        path.append(node)
        start, end = 1 << (depth - 1), (1 << depth) - 1
        node = (start + end - node) // 2
        depth -= 1
    path.reverse()
    return path


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(path):
    return "[" + ",".join(str(x) for x in path) + "]"


def main():
    global seed
    for label in [14, 26, 1, 2, 3, 4, 7, 8, 15, 16, 100, 1000000]:
        print(f"{label}: {show(path_in_zig_zag_tree(label))}")
    total = 0
    check = 0
    for label in range(1, 16384):
        for x in path_in_zig_zag_tree(label):
            total += x
            check = (check * 31 + x) % 1000000007
    print(f"labels 1 to 16383: path labels total {total}, checksum {check}")
    seed = 1104
    steps = 0
    check = 0
    for _ in range(2000):
        hi = next_random()
        label = (hi * 32768 + next_random()) % 1000000 + 1
        path = path_in_zig_zag_tree(label)
        steps += len(path)
        for x in path:
            check = (check * 31 + x) % 1000000007
    print(f"2000 random labels: {steps} nodes on their paths, checksum {check}")


main()
