# benchmark's Python mirror of tiles.kara (LeetCode #2209, the ★ arm): a
# table best[j][i], the fewest white tiles left visible among the first i
# tiles with j carpets, filled row by row.


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


seed = 2209


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    floors = []
    for f in range(8):
        white_in_8 = f % 7 + 1
        floors.append("".join("1" if next_random() % 8 < white_in_8 else "0" for _ in range(1000)))
    # each floor asked 40 times, carpets 10 to 249, each 1 to 20 long
    check = 0
    for q in range(40):
        for f in range(8):
            carpets = 10 + (q * 37 + f * 11) % 240
            length = 1 + (q * 7 + f * 3) % 20
            check = (check * 31 + minimum_white_tiles(floors[f], carpets, length)) % 1000000007
    print(f"40 passes over 8 floors: checksum {check}")


main()
