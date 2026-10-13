# LeetCode #498: Diagonal Traverse -- walking the zigzag.
# Mirrors diagonal_traverse.kara (the ★ arm); output is byte-identical.


def find_diagonal_order(mat):
    m = len(mat)
    n = len(mat[0])
    out = []
    r = 0
    c = 0
    up = True
    while len(out) < m * n:
        out.append(mat[r][c])
        if up:
            if c == n - 1:
                r += 1
                up = False
            elif r == 0:
                c += 1
                up = False
            else:
                r -= 1
                c += 1
        else:
            if r == m - 1:
                c += 1
                up = True
            elif c == 0:
                r += 1
                up = True
            else:
                r += 1
                c -= 1
    return out


def fmt(v):
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    return str(v)


def show(name, mat):
    print(f"{name}: {fmt(mat)} -> {fmt(find_diagonal_order(mat))}")


seed = 498


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    show("example 2", [[1, 2], [3, 4]])
    show("one cell", [[-100000]])
    show("one row", [[1, 2, 3, 4, 5]])
    show("one column", [[1], [2], [3], [4]])
    show("wide", [[1, 2, 3, 4], [5, 6, 7, 8]])
    show("tall", [[1, 2], [3, 4], [5, 6], [7, 8]])
    show("three by five", [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
    count = 300
    cells = 0
    checksum = 0
    for _ in range(count):
        m = 1 + next_random() % 12
        n = 1 + next_random() % 12
        mat = []
        for _ in range(m):
            row = []
            for _ in range(n):
                row.append(next_random() % 200001 - 100000)
            mat.append(row)
        for v in find_diagonal_order(mat):
            cells += 1
            checksum = (checksum * 31 + v + 100000) % 1000000007
    print(f"{count} random matrices: {cells} cells, checksum {checksum}")


main()
