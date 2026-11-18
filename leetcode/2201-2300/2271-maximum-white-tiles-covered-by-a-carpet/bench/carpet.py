# LeetCode #2271: Maximum White Tiles Covered by a Carpet -- the bench,
# the ★ arm.


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


# ---- bench harness ---------------------------------------------------------

seed = 2271


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(30):
        tiles = []
        at = 1
        for _ in range(50000):
            at += next_random() % 10001
            end = at + next_random() % 10000
            tiles.append([at, end])
            at = end + 1
        for i in range(49999, 0, -1):
            k = next_random() % (i + 1)
            tiles[i], tiles[k] = tiles[k], tiles[i]
        carpet_len = [1000, 1000000, 1000000000][t % 3]
        check = (check * 31 + maximum_white_tiles(tiles, carpet_len)) % 1000000007
    print(f"30 sets of 5 * 10^4: checksum {check}")


main()
