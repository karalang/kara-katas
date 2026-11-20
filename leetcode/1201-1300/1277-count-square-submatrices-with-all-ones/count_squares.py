# LeetCode #1277: Count Square Submatrices with All Ones -- Python mirror of
# the ★ arm: by dynamic programming over the sides of the largest squares.


def count_squares(matrix):
    m = len(matrix)
    n = len(matrix[0])
    side = [[0] * n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 1:
                side[i][j] = 1 if i == 0 or j == 0 else min(side[i - 1][j], side[i][j - 1], side[i - 1][j - 1]) + 1
                total += side[i][j]
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_matrix(m, n, percent):
    return [[1 if next_random() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]


def main():
    global seed
    print(f"{count_squares([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]])} {count_squares([[1, 0, 1], [1, 1, 0], [1, 1, 0]])}")
    seed = 1277
    total = 0
    check = 0
    for case in range(2000):
        m = next_random() % 12 + 1
        n = next_random() % 12 + 1
        percent = 50 if case % 3 == 0 else 80 if case % 3 == 1 else 95
        got = count_squares(random_matrix(m, n, percent))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random matrices: {total} squares, checksum {check}")
    ones = [[1] * 300 for _ in range(300)]
    dense = random_matrix(300, 300, 90)
    row = [[1] * 300]
    column = [[1] for _ in range(300)]
    print(f"{count_squares(ones)} {count_squares(dense)} {count_squares(row)} {count_squares(column)}")


main()
