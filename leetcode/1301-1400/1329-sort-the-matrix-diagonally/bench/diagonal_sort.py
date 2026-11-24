# LeetCode #1329 bench, Python mirror of the Kāra bench: the ★ arm (each
# diagonal read into a list, sorted and written back) on 8 matrices of 300
# by 300, values 1 to 100, built once. Then 100 passes, each setting one
# cell of every matrix from the checksum so far, answering it and folding
# two of the answer's cells plus the pass into the checksum.


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


def main():
    size = 300
    mats = [[[1 + next_random() % 100 for _ in range(size)] for _ in range(size)] for _ in range(8)]
    check = 0
    for p in range(100):
        for t in range(8):
            r = check % size
            c = (check // 7) % size
            mats[t][r][c] = 1 + (check // 13) % 100
            out = diagonal_sort(mats[t])
            check = (check * 31 + out[r][c] + out[size - 1][size // 2] + p) % 1000000007
    print(f"100 passes over 8 matrices of 300 by 300: checksum {check}")


main()
