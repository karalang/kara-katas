# LeetCode #1289 bench, in Python: the ★ arm (the row above's two smallest
# path sums) on 100 grids of 200 by 200, built once, 300 rounds.

BIG = 2**63 - 1


def min_falling_path_sum(grid):
    first, first_col, second = 0, -1, 0
    for row in grid:
        next_first, next_col, next_second = BIG, -1, BIG
        for j, x in enumerate(row):
            s = x + (second if j == first_col else first)
            if s < next_first:
                next_second = next_first
                next_first = s
                next_col = j
            elif s < next_second:
                next_second = s
        first, first_col, second = next_first, next_col, next_second
    return first


seed = 1289


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def problem(n):
    return [[next_random() % 199 - 99 for _ in range(n)] for _ in range(n)]


def main():
    grids = [problem(200) for _ in range(100)]
    check = 0
    for rnd in range(300):
        for grid in grids:
            check = (check * 131 + min_falling_path_sum(grid) + rnd + 1000000) % 1000000007
    print(f"300 rounds of 100 grids of 200 by 200: checksum {check}")


if __name__ == "__main__":
    main()
