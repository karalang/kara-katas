# LeetCode #2379: Minimum Recolors to Get K Consecutive Black Blocks --
# Python mirror of the ★ arm, a sliding window.


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
    print(f"{minimum_recolors('WBBWWBBWBW', 7)} {minimum_recolors('WBWBBBW', 2)}")
    print(f"{minimum_recolors('W', 1)}")
    white = "W" * 100
    turns = "".join("B" if i % 2 == 0 else "W" for i in range(100))
    total = sum(minimum_recolors(turns, k) for k in range(1, 101))
    print(f"{minimum_recolors(white, 100)} {total}")
    check = 0
    none = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        chance = next_random() % 10
        k = 1 + next_random() % n
        letters = "".join("W" if next_random() % 10 < chance else "B" for _ in range(n))
        t = minimum_recolors(letters, k)
        check = (check * 31 + t) % 1000000007
        if t == 0:
            none += 1
    print(f"2000 strings: checksum {check}, {none} need no recoloring")


main()
