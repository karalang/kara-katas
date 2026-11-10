# LeetCode #2088: Count Fertile Pyramids in a Land -- Python mirror of the
# ★ arm (pyramids.kara): the tallest plot apexed at each cell from the row
# before it, bottom up for the pyramids and top down for the inverse.

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
        tall = [0] * n
        for c in range(n):
            if grid[r][c] == 0:
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


def random_land(m, n, odds):
    return [[1 if next_random() % 10 < odds else 0 for _ in range(n)] for _ in range(m)]


def show(grid):
    return "/".join("".join(str(x) for x in r) for r in grid)


def main():
    examples = [
        [[0, 1, 1, 0], [1, 1, 1, 1]],
        [[1, 1, 1], [1, 1, 1]],
        [[1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 0, 0, 1]],
        [[1]],
        [[1, 1, 1]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
    ]
    for g in examples:
        print(f"{show(g)} -> {count_pyramids(g)}")
    total = check = 0
    for _ in range(2000):
        m = next_random() % 12 + 1
        n = next_random() % 12 + 1
        odds = next_random() % 5 + 5
        a = count_pyramids(random_land(m, n, odds))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 lands: sum {total}, checksum {check}")
    mostly = [[1 if next_random() % 20 < 19 else 0 for _ in range(316)] for _ in range(316)]
    print(f"316 by 316, 19 in 20 fertile: {count_pyramids(mostly)}")
    print(f"100 by 1000, 9 in 10 fertile: {count_pyramids(random_land(100, 1000, 9))}")

main()
