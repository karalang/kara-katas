# LeetCode #1329: Sort the Matrix Diagonally -- Python mirror of the ★ arm
# and its harness.


def sort_from(out, i0, j0):
    m, n = len(out), len(out[0])
    vals = []
    k = 0
    while i0 + k < m and j0 + k < n:
        vals.append(out[i0 + k][j0 + k])
        k += 1
    vals.sort()
    for k, v in enumerate(vals):
        out[i0 + k][j0 + k] = v


def diagonal_sort(mat):
    out = [row[:] for row in mat]
    for i in range(len(mat)):
        sort_from(out, i, 0)
    for j in range(1, len(mat[0])):
        sort_from(out, 0, j)
    return out


seed = 1329


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(mat):
    return "".join("[" + ",".join(str(v) for v in row) + "]" for row in mat)


def fold(check, mat):
    c = check
    for row in mat:
        for v in row:
            c = (c * 131 + v) % 1000000007
        c = (c * 131 + 101) % 1000000007
    return c


def main():
    ex1 = [[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]
    ex2 = [
        [11, 25, 66, 1, 69, 7],
        [23, 55, 17, 45, 15, 52],
        [75, 31, 36, 44, 58, 8],
        [22, 27, 33, 25, 68, 4],
        [84, 28, 14, 11, 5, 50],
    ]
    print(show(diagonal_sort(ex1)))
    print(show(diagonal_sort(ex2)))
    print(f"{show(diagonal_sort([[7]]))} {show(diagonal_sort([[5, 4, 3]]))} {show(diagonal_sort([[3], [2], [1]]))}")
    big = [[100 - (i * 7 + j) % 100 for j in range(100)] for i in range(100)]
    s = diagonal_sort(big)
    print(f"100 by 100: corners {s[0][0]} {s[0][99]} {s[99][0]} {s[99][99]}, checksum {fold(0, s)}")
    check = 0
    cells = 0
    for t in range(300):
        if t % 10 == 0:
            m = 1 + next_random() % 100
            n = 1 + next_random() % 100
        else:
            m = 1 + next_random() % 8
            n = 1 + next_random() % 8
        top = 100 if t % 3 == 0 else 3 if t % 3 == 1 else 1
        mat = [[1 + next_random() % top for _ in range(n)] for _ in range(m)]
        cells += m * n
        check = fold(check, diagonal_sort(mat))
    print(f"300 random matrices: {cells} cells, checksum {check}")


main()
