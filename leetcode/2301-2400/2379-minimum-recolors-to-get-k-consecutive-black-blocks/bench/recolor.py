# LeetCode #2379: Minimum Recolors to Get K Consecutive Black Blocks --
# the bench, the ★ arm in Python: the whites of the first window counted,
# then the window slid along one block at a time.


def minimum_recolors(blocks, k):
    whites = 0
    for i in range(k):
        if blocks[i] == "W":
            whites += 1
    fewest = whites
    for i in range(k, len(blocks)):
        if blocks[i] == "W":
            whites += 1
        if blocks[i - k] == "W":
            whites -= 1
        fewest = min(fewest, whites)
    return fewest


seed = 2379


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1000 strings of 100 blocks, string s white with a chance of s % 10
    # in 10; pass p asks string s for k = 1 + (7 p + s) % 100
    strings = []
    for s in range(1000):
        strings.append("".join("W" if next_random() % 10 < s % 10 else "B" for _ in range(100)))
    check = 0
    for p in range(500):
        for s in range(1000):
            k = 1 + (7 * p + s) % 100
            check = (check * 31 + minimum_recolors(strings[s], k) + p) % 1000000007
    print(f"500 passes over 1000 strings of 100 blocks: checksum {check}")


main()
