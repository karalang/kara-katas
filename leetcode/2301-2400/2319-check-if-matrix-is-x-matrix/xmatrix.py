# LeetCode #2319: Check if Matrix Is X-Matrix -- the Python mirror of the
# ★ arm. One walk over the cells: a cell on either diagonal must be
# nonzero and any other must be zero.

seed = 2319


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def check_x_matrix(grid):
    n = len(grid)
    for i in range(n):
        for j in range(n):
            on = i == j or i + j == n - 1
            if on != (grid[i][j] != 0):
                return False
    return True


def grid_of(n, slips):
    g = []
    for i in range(n):
        row = []
        for j in range(n):
            on = i == j or i + j == n - 1
            slip = next_random() % slips == 0
            value = next_random() % 100000 + 1
            row.append(value if on != slip else 0)
        g.append(row)
    return g


def show(b):
    print("true" if b else "false")


show(check_x_matrix([[2, 0, 0, 1], [0, 3, 1, 0], [0, 5, 2, 0], [4, 0, 0, 2]]))
show(check_x_matrix([[5, 7, 0], [0, 3, 1], [0, 5, 0]]))
show(check_x_matrix([[1, 0, 1], [0, 1, 0], [1, 0, 1]]))
show(check_x_matrix([[1, 0, 1], [0, 0, 0], [1, 0, 1]]))
show(check_x_matrix([[1, 0, 1], [0, 1, 1], [1, 0, 1]]))
big = grid_of(100, 1000000)
show(check_x_matrix(big))
big[37][50] = 9
show(check_x_matrix(big))
check = 0
xs = 0
for _ in range(2000):
    n = next_random() % 6 + 3
    slips = next_random() % 181 + 20
    is_x = check_x_matrix(grid_of(n, slips))
    check = (check * 31 + (2 if is_x else 1)) % 1000000007
    if is_x:
        xs += 1
print(f"2000 grids: checksum {check}, {xs} X-matrices")
