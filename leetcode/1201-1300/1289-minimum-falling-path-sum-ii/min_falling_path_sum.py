# LeetCode #1289: Minimum Falling Path Sum II -- Python mirror of the ★ arm:
# the row above's two smallest path sums.

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def problem(n):
    return [[next_random() % 199 - 99 for _ in range(n)] for _ in range(n)]


def main():
    global seed
    f = min_falling_path_sum
    print(f"{f([[1, 2, 3], [4, 5, 6], [7, 8, 9]])} {f([[7]])} {f([[1, 1], [1, 1]])} {f([[-5, -5, 3], [-5, 2, -5], [0, -5, -5]])}")
    seed = 1289
    total = check = 0
    for case in range(303):
        n = next_random() % 30 + 1 if case < 300 else 200
        best = f(problem(n))
        total += best
        check = (check * 131 + best + 1000000) % 1000000007
    print(f"303 random grids: total {total}, checksum {check}")


if __name__ == "__main__":
    main()
