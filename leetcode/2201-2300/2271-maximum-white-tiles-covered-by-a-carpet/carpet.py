# LeetCode #2271: Maximum White Tiles Covered by a Carpet -- the Python
# mirror of the ★ arm, `carpet.kara`, line for line. Its output is
# byte-identical.


def maximum_white_tiles(tiles, carpet_len):
    s = sorted(tiles)
    m = len(s)
    best = 0
    whole = 0
    j = 0
    for i in range(m):
        end = s[i][0] + carpet_len - 1
        while j < m and s[j][1] <= end:
            whole += s[j][1] - s[j][0] + 1
            j += 1
        part = end - s[j][0] + 1 if j < m and s[j][0] <= end else 0
        best = max(best, whole + part)
        if j > i:
            whole -= s[i][1] - s[i][0] + 1
        else:
            j = i + 1
    return best


seed = 2271


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tiles(m, long, gap):
    tiles = []
    at = 1
    for _ in range(m):
        at += next_random() % (gap + 1)
        end = at + next_random() % long
        tiles.append([at, end])
        at = end + 1
    for i in range(m - 1, 0, -1):
        k = next_random() % (i + 1)
        tiles[i], tiles[k] = tiles[k], tiles[i]
    return tiles


def show(tiles):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in tiles) + "]"


def main():
    examples = [
        ([[1, 5], [10, 11], [12, 18], [20, 25], [30, 32]], 10),
        ([[10, 11], [1, 1]], 2),
        ([[1, 100]], 7),
        ([[5, 6]], 7),
        ([[1, 3], [4, 6], [7, 9]], 5),
        ([[8, 8], [2, 4]], 1),
        ([[1, 2], [1000, 1003], [1005, 1005]], 1000),
    ]
    for tiles, carpet_len in examples:
        print(f"{show(tiles)}, {carpet_len} -> {maximum_white_tiles(tiles, carpet_len)}")
    check = 0
    for t in range(2000):
        m = next_random() % 12 + 1
        tiles = random_tiles(m, [1, 5, 20][t % 3], [0, 3, 30][t // 3 % 3])
        carpet_len = next_random() % 60 + 1
        check = (check * 31 + maximum_white_tiles(tiles, carpet_len)) % 1000000007
    print(f"2000 sets: checksum {check}")
    big = random_tiles(50000, 10000, 10000)
    answers = [maximum_white_tiles(big, 1000), maximum_white_tiles(big, 1000000), maximum_white_tiles(big, 1000000000)]
    print(f"5 * 10^4 tiles: [{', '.join(map(str, answers))}]")


main()
