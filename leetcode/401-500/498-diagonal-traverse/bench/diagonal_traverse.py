# Benchmark for #498: Python mirror of the ★ arm (walking the zigzag);
# see diagonal_traverse.kara.


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


seed = 498


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100 matrices of 10,000 cells (the problem's most), in ten shapes
    # from 1 by 10,000 to 10,000 by 1, with values from -100,000 to
    # 100,000, built once. Then each is traversed 100 times; every
    # traversal is folded into the checksum, each value weighed by its
    # place.
    rows = [1, 4, 10, 25, 50, 100, 200, 400, 1000, 10000]
    all_mats = []
    for k in range(100):
        m = rows[k % 10]
        n = 10000 // m
        mat = []
        for _ in range(m):
            mat.append([next_random() % 200001 - 100000 for _ in range(n)])
        all_mats.append(mat)
    checksum = 0
    for _ in range(100):
        for k in range(100):
            order = find_diagonal_order(all_mats[k])
            s = 0
            for i in range(len(order)):
                s += order[i] * (i % 7 + 1)
            checksum = (checksum * 31 + s % 1000000007 + 1000000007) % 1000000007
    print(f"100 matrices of 10000 cells, 100 times each: checksum {checksum}")


main()
