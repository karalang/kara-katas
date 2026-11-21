# LeetCode #2435: Paths in Matrix Whose Sum Is Divisible by K -- the
# Python mirror of the ★ arm: one row of counts by remainder, each cell's
# from above, still in place, and from the left, shifted by its value.

MOD = 1000000007
seed = 2435


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_paths(grid, k):
    n = len(grid[0])
    row = [[0] * k for _ in range(n)]
    for i in range(len(grid)):
        for j in range(n):
            came = [0] * k
            if i == 0 and j == 0:
                came[0] = 1
            for r in range(k):
                left = row[j - 1][r] if j > 0 else 0
                came[r] = (came[r] + row[j][r] + left) % MOD
            v = grid[i][j]
            for r in range(k):
                row[j][(r + v) % k] = came[r]
    return row[n - 1][0]


def random_grid(m, n, top):
    return [[next_random() % (top + 1) for _ in range(n)] for _ in range(m)]


def main():
    cases = [
        ([[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3),
        ([[0, 0]], 5),
        ([[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], 1),
        ([[50]], 50),
        ([[49]], 50),
        ([[0, 0], [0, 0]], 7),
    ]
    for grid, k in cases:
        print(f"{len(grid)} by {len(grid[0])}, k = {k}: {number_of_paths(grid, k)}")
    print(f"200 by 250, k = 50: {number_of_paths(random_grid(200, 250, 100), 50)}")
    print(f"2 by 25000, k = 17: {number_of_paths(random_grid(2, 25000, 100), 17)}")
    full = [[100] * 200 for _ in range(250)]
    print(f"250 by 200 of 100, k = 1: {number_of_paths(full, 1)}")
    check = 0
    total = 0
    for _ in range(3000):
        m = 1 + next_random() % 4
        n = 1 + next_random() % 4
        k = 1 + next_random() % 6
        answer = number_of_paths(random_grid(m, n, 9), k)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
