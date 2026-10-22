# LeetCode #861: Score After Flipping Matrix -- Python mirror of the bench
# program (the ★ arm, count each column against the first).


def matrix_score(grid):
    m = len(grid)
    n = len(grid[0])
    score = 0
    for j in range(n):
        ones = 0
        for row in grid:
            if row[j] == row[0]:
                ones += 1
        score = score * 2 + max(ones, m - ones)
    return score


seed = 861


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 20
    rounds = 1000000
    grid = [[next_random() % 2 for _ in range(size)] for _ in range(size)]
    total = 0
    check = 0
    for _ in range(rounds):
        cell = next_random() % (size * size)
        i = cell // size
        j = cell % size
        grid[i][j] = 1 - grid[i][j]
        s = matrix_score(grid)
        grid[i][j] = 1 - grid[i][j]
        total += s
        check = (check * 31 + s) % 1000000007
    print(f"{rounds} rounds on a {size} by {size} grid: scores sum to {total}, checksum {check}")


main()
