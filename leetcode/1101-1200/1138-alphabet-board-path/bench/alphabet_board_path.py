# LeetCode #1138: Alphabet Board Path -- the bench, the ★ arm's algorithm:
# coordinates, up and left first, down and right after.


def alphabet_board_path(target):
    path = []
    row = col = 0
    for c in target:
        k = ord(c) - ord("a")
        r, k_col = k // 5, k % 5
        path.append("U" * max(row - r, 0))
        path.append("L" * max(col - k_col, 0))
        path.append("D" * max(r - row, 0))
        path.append("R" * max(k_col - col, 0))
        path.append("!")
        row, col = r, k_col
    return "".join(path)


seed = 1138


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    targets = [[letters[next_random() % 26] for _ in range(100)] for _ in range(1000)]
    total = 0
    check = 0
    for rnd in range(100):
        for j in range(1000):
            targets[j][(rnd * 37 + j) % 100] = letters[next_random() % 26]
            target = "".join(targets[j])
            path = alphabet_board_path(target)
            mid = ord(path[len(path) // 2])
            total += len(path)
            check = (check * 31 + len(path) * 128 + mid) % 1000000007
    print(f"100 rounds over 1000 targets of 100 letters: lengths total {total}, checksum {check}")


main()
