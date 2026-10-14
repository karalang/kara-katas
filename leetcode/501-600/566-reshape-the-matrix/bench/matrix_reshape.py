# Benchmark for #566: Python mirror of the ★ arm (index arithmetic); see
# matrix_reshape.kara.


def matrix_reshape(mat, r, c):
    m = len(mat)
    n = len(mat[0])
    if m * n != r * c:
        return [row[:] for row in mat]
    out = []
    for i in range(r):
        row = []
        for j in range(c):
            k = i * c + j
            row.append(mat[k // n][k % n])
        out.append(row)
    return out


# ---- benchmark ---------------------------------------------------------------

seed = 566


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    rounds = 800
    shapes = [(1, 10000), (4, 2500), (25, 400), (50, 200), (100, 100), (200, 50), (400, 25), (2500, 4), (10000, 1), (99, 101)]
    mats = [[[step() % 2001 - 1000 for _ in range(100)] for _ in range(100)] for _ in range(count)]
    cells = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            r, c = shapes[(rnd + g) % 10]
            got = matrix_reshape(mats[(rnd * 7 + g) % count], r, c)
            rows = len(got)
            cols = len(got[0])
            cells += rows * cols
            checksum = (checksum * 31 + got[rnd % rows][g % cols] + 1000) % 1000000007
    print(f"{count} matrices of 100 by 100, {rounds} rounds: {cells} cells, checksum {checksum}")


main()
