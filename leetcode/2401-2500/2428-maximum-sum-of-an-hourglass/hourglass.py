# LeetCode #2428: Maximum Sum of an Hourglass -- the Python mirror of the
# ★ arm: every centre off the border, its seven cells added directly.

seed = 2428


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_sum(grid):
    m = len(grid)
    n = len(grid[0])
    best = 0
    for r in range(1, m - 1):
        for c in range(1, n - 1):
            total = (grid[r - 1][c - 1] + grid[r - 1][c] + grid[r - 1][c + 1]
                     + grid[r][c]
                     + grid[r + 1][c - 1] + grid[r + 1][c] + grid[r + 1][c + 1])
            best = max(best, total)
    return best


def random_grid(m, n, top):
    grid = []
    for _ in range(m):
        row = []
        for _ in range(n):
            a = next_random()
            row.append((a * 32768 + next_random()) % (top + 1))
        grid.append(row)
    return grid


def main():
    print(max_sum([[6, 2, 1, 3], [4, 2, 1, 5], [9, 2, 8, 7], [4, 1, 2, 9]]))
    print(max_sum([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(max_sum([[0] * 3 for _ in range(3)]))
    print(max_sum([[1000000] * 150 for _ in range(150)]))
    print(max_sum(random_grid(150, 150, 1000000)))
    print(max_sum(random_grid(3, 150, 1000000)))
    print(max_sum(random_grid(150, 3, 1000000)))
    check = 0
    total = 0
    for _ in range(3000):
        m = 3 + next_random() % 4
        n = 3 + next_random() % 4
        answer = max_sum(random_grid(m, n, 9))
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
