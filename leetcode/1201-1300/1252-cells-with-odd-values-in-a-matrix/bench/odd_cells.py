# LeetCode #1252 bench, in Python: the ★ arm (the matrix itself, every
# cell of each place's row and column raised by one, then the odd cells
# counted) on 1000 random lists of 100 places in a 50 by 50 matrix built
# once, each asked 40 times; every count folded into a checksum.


def odd_cells(m, n, indices):
    matrix = [[0] * n for _ in range(m)]
    for r, c in indices:
        for j in range(n):
            matrix[r][j] += 1
        for i in range(m):
            matrix[i][c] += 1
    odd = 0
    for row in matrix:
        for v in row:
            if v % 2 == 1:
                odd += 1
    return odd


seed = 1252


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(1000):
        indices = []
        for _ in range(100):
            r = next_random() % 50
            c = next_random() % 50
            indices.append([r, c])
        cases.append(indices)
    check = 0
    for _ in range(40):
        for indices in cases:
            check = (check * 131 + odd_cells(50, 50, indices)) % 1000000007
    print(f"40 rounds of 1000 lists of 100 places in 50 by 50: checksum {check}")


main()
