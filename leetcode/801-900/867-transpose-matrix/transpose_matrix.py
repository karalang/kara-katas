# LeetCode #867: Transpose Matrix -- Python mirror of the ★ arm (one column
# at a time).

M = 1000000007


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    out = []
    for c in range(cols):
        out.append([matrix[r][c] for r in range(rows)])
    return out


seed = 867


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 2000000001 - 1000000000


def random_matrix(rows, cols):
    return [[random_value() for _ in range(cols)] for _ in range(rows)]


def show_matrix(m):
    return "[" + ",".join("[" + ",".join(str(v) for v in row) + "]" for row in m) + "]"


def fold(check, m):
    for row in m:
        for v in row:
            check = (check * 31 + v % M + M) % M
        check = (check * 31 + 7) % M
    return check


def summary(m):
    return f"{len(m)} x {len(m[0])}, checksum {fold(0, m)}"


def show(m):
    print(f"matrix = {show_matrix(m)} -> {show_matrix(transpose(m))}")


def main():
    show([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    show([[1, 2, 3], [4, 5, 6]])
    show([[5]])
    show([[1, 2, 3, 4]])
    show([[1], [2], [3], [4]])
    show([[-1000000000, 1000000000], [0, -7]])
    show([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    for rows, cols in [(100000, 1), (1, 100000), (1000, 100), (316, 316)]:
        m = random_matrix(rows, cols)
        print(f"{summary(m)} -> {summary(transpose(m))}")
    entries = 0
    check = 0
    for _ in range(1000):
        rows = 1 + next_random() % 20
        cols = 1 + next_random() % 20
        t = transpose(random_matrix(rows, cols))
        entries += len(t) * len(t[0])
        check = fold(check, t)
    print(f"1000 random matrices: {entries} entries, checksum {check}")


main()
