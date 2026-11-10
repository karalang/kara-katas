# LeetCode #2088: Count Fertile Pyramids in a Land -- Python mirror of the
# ★ arm's benchmark (pyramids.kara): the same 20 lands, each counted 20
# times by the same two passes over lists.

seed = 2088


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_one_way(grid, order):
    n = len(grid[0])
    below = [0] * n
    count = 0
    for r in order:
        row = grid[r]
        tall = [0] * n
        for c in range(n):
            if row[c] == 0:
                continue
            if c == 0 or c == n - 1:
                tall[c] = 1
            else:
                tall[c] = min(below[c - 1], below[c], below[c + 1]) + 1
            count += tall[c] - 1
        below = tall
    return count


def count_pyramids(grid):
    m = len(grid)
    return count_one_way(grid, range(m - 1, -1, -1)) + count_one_way(grid, range(m))


def main():
    lands = []
    for t in range(20):
        odds = 15 + t % 5
        lands.append([[1 if next_random() % 20 < odds else 0 for _ in range(316)] for _ in range(316)])
    total = check = 0
    for rnd in range(20):
        for t in range(20):
            a = count_pyramids(lands[(t + rnd) % 20])
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"400 counts: sum {total}, checksum {check}")


main()
