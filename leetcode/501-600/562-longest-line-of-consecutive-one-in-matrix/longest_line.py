# LeetCode #562: Longest Line of Consecutive One in Matrix -- Python
# mirror of the ★ arm (one row of running counts); see longest_line.kara.


def longest_line(mat):
    n = len(mat[0])
    up = [0] * n
    diag = [0] * n
    anti = [0] * n
    best = 0
    for row in mat:
        next_up = [0] * n
        next_diag = [0] * n
        next_anti = [0] * n
        across = 0
        for j in range(n):
            if row[j] == 1:
                across += 1
                next_up[j] = up[j] + 1
                next_diag[j] = diag[j - 1] + 1 if j > 0 else 1
                next_anti[j] = anti[j + 1] + 1 if j + 1 < n else 1
                best = max(best, across, next_up[j], next_diag[j], next_anti[j])
            else:
                across = 0
        up, diag, anti = next_up, next_diag, next_anti
    return best


# ---- test harness ---------------------------------------------------------

seed = 562


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(mat):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in mat) + "]"


def show(mat):
    print(f"{fmt(mat)}: {longest_line(mat)}")


def random_matrix(m, n, percent):
    return [[1 if step() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]


def main():
    show([[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 1]])
    show([[1, 1, 1, 1], [0, 1, 1, 0], [0, 0, 0, 1]])
    show([[0]])
    show([[1]])
    show([[1, 1, 0, 1, 1, 1]])
    show([[1], [1], [0], [1]])
    show([[1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [0, 0, 0, 1]])
    show([[0, 0, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 1]])
    total = 0
    checksum = 0
    for _ in range(300):
        m = 1 + step() % 12
        n = 1 + step() % 12
        percent = 30 + step() % 61
        got = longest_line(random_matrix(m, n, percent))
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random matrices: total {total}, checksum {checksum}")
    print(f"100 by 100 ones: {longest_line(random_matrix(100, 100, 100))}")
    print(f"1 by 10000 ones: {longest_line(random_matrix(1, 10000, 100))}")
    print(f"10000 by 1 ones: {longest_line(random_matrix(10000, 1, 100))}")
    print(f"100 by 100 random: {longest_line(random_matrix(100, 100, 70))}")


main()
