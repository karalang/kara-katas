# LeetCode #1104: Path In Zigzag Labelled Binary Tree -- the bench in
# Python: the ★ arm (walking up, each parent half the label's mirror in
# its row) over every label from 1 to 10^6 in a different order each of
# 8 rounds.


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


def main():
    nodes = 0
    check = 0
    for rnd in range(8):
        for i in range(1000000):
            label = (i * 7919 + rnd * 104729) % 1000000 + 1
            path = path_in_zig_zag_tree(label)
            nodes += len(path)
            check = (check * 31 + path[len(path) // 2]) % 1000000007
    print(f"8 rounds over the labels 1 to 10^6: {nodes} nodes on their paths, checksum {check}")


main()
