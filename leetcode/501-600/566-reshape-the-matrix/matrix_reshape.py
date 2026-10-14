# LeetCode #566: Reshape the Matrix -- Python mirror of the ★ arm (index
# arithmetic); see matrix_reshape.kara.


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


# ---- test harness ---------------------------------------------------------

seed = 566


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text(mat):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in mat) + "]"


def show(mat, r, c):
    print(f"{text(mat)} to {r} by {c}: {text(matrix_reshape(mat, r, c))}")


def main():
    show([[1, 2], [3, 4]], 1, 4)
    show([[1, 2], [3, 4]], 2, 4)
    show([[1, 2], [3, 4]], 2, 2)
    show([[7]], 1, 1)
    show([[1, 2, 3, 4, 5, 6]], 6, 1)
    show([[1], [2], [3], [4], [5], [6]], 1, 6)
    show([[1, 2, 3], [4, 5, 6]], 3, 2)
    show([[-1000, 1000], [1000, -1000]], 4, 1)
    show([[1, 2, 3], [4, 5, 6]], 5, 1)
    kept = 0
    checksum = 0
    for t in range(300):
        m = 1 + step() % 8
        n = 1 + step() % 8
        mat = [[step() % 2001 - 1000 for _ in range(n)] for _ in range(m)]
        r = 1 + step() % (m * n)
        while (m * n) % r != 0:
            r -= 1
        c = m * n // r
        if t % 4 == 3:
            c += 1
        got = matrix_reshape(mat, r, c)
        if len(got) == m and len(got[0]) == n and not (r == m and c == n):
            kept += 1
        for row in got:
            for x in row:
                checksum = (checksum * 31 + x + 1000) % 1000000007
            checksum = (checksum * 31 + 7) % 1000000007
    print(f"300 random matrices: {kept} kept, checksum {checksum}")
    big = [[(i * 100 + j) % 2001 - 1000 for j in range(100)] for i in range(100)]
    wide = matrix_reshape(big, 1, 10000)
    tall = matrix_reshape(wide, 10000, 1)
    back = matrix_reshape(tall, 100, 100)
    same = "true" if back == big else "false"
    print(f"100 by 100: wide {len(wide)} by {len(wide[0])}, tall {len(tall)} by {len(tall[0])}, back the same {same}")


main()
