# LeetCode #2267: Check if There Is a Valid Parentheses String Path --
# the Python mirror of the ★ arm, `path.kara`, line for line. Its output
# is byte-identical.


def has_valid_path(grid):
    m = len(grid)
    n = len(grid[0])
    if (m + n - 1) % 2 == 1 or grid[0][0] == ')' or grid[m - 1][n - 1] == '(':
        return False
    most = (m + n) // 2 + 1
    reach = [[[False] * (most + 1) for _ in range(n)] for _ in range(m)]
    reach[0][0][1] = True
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            step = 1 if grid[i][j] == '(' else -1
            for b in range(most + 1):
                frm = b - step
                if frm < 0 or frm > most:
                    continue
                if (i > 0 and reach[i - 1][j][frm]) or (j > 0 and reach[i][j - 1][frm]):
                    reach[i][j][b] = True
    return reach[m - 1][n - 1][0]


seed = 2267


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, open_):
    return [['(' if next_random() % 100 < open_ else ')' for _ in range(n)] for _ in range(m)]


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        ["(((", ")()", "(()", "(()"],
        ["))", "(("],
        ["("],
        ["()"],
        ["(", ")"],
        ["((", "))"],
        [")(", "()"],
    ]
    for rows in examples:
        print(f"[{', '.join(rows)}] -> {show(has_valid_path([list(r) for r in rows]))}")
    found = 0
    check = 0
    for t in range(2000):
        m = next_random() % 8 + 1
        n = next_random() % 8 + 1
        valid = has_valid_path(random_grid(m, n, [50, 60][t % 2]))
        if valid:
            found += 1
        check = (check * 31 + (2 if valid else 1)) % 1000000007
    print(f"2000 grids: {found} with a path, checksum {check}")
    rand = random_grid(100, 99, 55)
    checker = [['(' if (i + j) % 2 == 0 else ')' for j in range(99)] for i in range(100)]
    split = [['(' if i + j < 99 else ')' for j in range(99)] for i in range(100)]
    answers = [has_valid_path(rand), has_valid_path(checker), has_valid_path(split)]
    print(f"100 by 99: [{', '.join(show(a) for a in answers)}]")


main()
