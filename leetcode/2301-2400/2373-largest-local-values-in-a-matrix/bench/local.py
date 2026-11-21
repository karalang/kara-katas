# LeetCode #2373: Largest Local Values in a Matrix -- the bench, the ★ arm
# in Python: each cell of the answer is the largest of the nine values in
# the 3 x 3 block whose top left corner it names.


def largest_local(grid):
    n = len(grid)
    out = []
    for i in range(n - 2):
        row = []
        for j in range(n - 2):
            most = 0
            for di in range(3):
                for dj in range(3):
                    v = grid[i + di][j + dj]
                    if v > most:
                        most = v
            row.append(most)
        out.append(row)
    return out


SEED = [2373]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # grid a: 100 x 100 random values from 1 to 10 (a + 1)
    grids = []
    for a in range(10):
        grids.append([[1 + next_random() % (10 * (a + 1)) for _ in range(100)] for _ in range(100)])
    check = 0
    for p in range(200):
        for grid in grids:
            for row in largest_local(grid):
                for v in row:
                    check = (check * 31 + v + p) % 1000000007
    print(f"200 passes over 10 grids of 100 x 100: checksum {check}")


main()
