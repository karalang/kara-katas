# LeetCode #2267: Check if There Is a Valid Parentheses String Path --
# Python mirror of the ★ arm (path.kara) on the bench workload: a table
# reach[i][j][b] of the balances some path to (i, j) can end with. Output
# is byte-identical to path.kara.


def has_valid_path(grid):
    m = len(grid)
    n = len(grid[0])
    if (m + n - 1) % 2 == 1 or grid[0][0] == ")" or grid[m - 1][n - 1] == "(":
        return False
    most = (m + n) // 2 + 1
    reach = [[[False] * (most + 1) for _ in range(n)] for _ in range(m)]
    reach[0][0][1] = True
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            step = 1 if grid[i][j] == "(" else -1
            for b in range(most + 1):
                frm = b - step
                if frm < 0 or frm > most:
                    continue
                if (i > 0 and reach[i - 1][j][frm]) or (j > 0 and reach[i][j - 1][frm]):
                    reach[i][j][b] = True
    return reach[m - 1][n - 1][0]


# ---- bench harness ---------------------------------------------------------

seed = 2267


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    found = 0
    check = 0
    for t in range(20):
        open_ = 50 + t
        grid = [["(" if next_random() % 100 < open_ else ")" for _ in range(99)] for _ in range(100)]
        grid[0][0] = "("
        grid[99][98] = ")"
        valid = has_valid_path(grid)
        if valid:
            found += 1
        check = (check * 31 + (2 if valid else 1)) % 1000000007
    print(f"20 grids of 100 by 99: {found} with a path, checksum {check}")


main()
