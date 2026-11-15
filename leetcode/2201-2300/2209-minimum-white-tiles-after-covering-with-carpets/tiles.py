# Python mirror of tiles.kara (LeetCode #2209, the ★ arm): a table
# best[j][i], the fewest white tiles left visible among the first i tiles
# with j carpets, filled row by row: tile i - 1 is either left as it is,
# or the last of a carpet laid over tiles i - len to i - 1.


def minimum_white_tiles(floor, num_carpets, carpet_len):
    tiles = [1 if c == "1" else 0 for c in floor]
    n = len(tiles)
    best = [[0] * (n + 1) for _ in range(num_carpets + 1)]
    for j in range(num_carpets + 1):
        for i in range(1, n + 1):
            left = best[j][i - 1] + tiles[i - 1]
            if j == 0:
                best[j][i] = left
            else:
                best[j][i] = min(left, best[j - 1][max(i - carpet_len, 0)])
    return best[num_carpets][n]


# ---- test harness ---------------------------------------------------------

seed = 2209


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_floor(n, white_in_8):
    return "".join("1" if next_random() % 8 < white_in_8 else "0" for _ in range(n))


def show(floor, num_carpets, carpet_len):
    print(f'"{floor}", {num_carpets} of {carpet_len} -> {minimum_white_tiles(floor, num_carpets, carpet_len)}')


def main():
    # LeetCode's two examples, then four more: one tile, no white tile, a
    # carpet as long as the floor, and more carpets than the floor needs
    show("10110101", 2, 2)
    show("11111", 2, 3)
    show("1", 1, 1)
    show("0000", 1, 2)
    show("1101011", 1, 7)
    show("1010101", 9, 1)
    # 2000 random floors of 1 to 40 tiles, white 2, 4 and 7 times in 8
    check = 0
    for c in range(2000):
        n = next_random() % 40 + 1
        floor = random_floor(n, [2, 4, 7][c % 3])
        length = next_random() % n + 1
        carpets = next_random() % 6 + 1
        check = (check * 31 + minimum_white_tiles(floor, carpets, length)) % 1000000007
    print(f"2000 floors: checksum {check}")
    # the constraints' largest: 1000 tiles and 1000 carpets of 1; then the
    # same tiles under 100 carpets of 3, 30 of 7, and one of 999
    wide = random_floor(1000, 4)
    print(f"1000 carpets of 1 -> {minimum_white_tiles(wide, 1000, 1)}")
    print(f"100 carpets of 3 -> {minimum_white_tiles(wide, 100, 3)}")
    print(f"30 carpets of 7 -> {minimum_white_tiles(wide, 30, 7)}")
    print(f"one carpet of 999 -> {minimum_white_tiles(wide, 1, 999)}")


main()
