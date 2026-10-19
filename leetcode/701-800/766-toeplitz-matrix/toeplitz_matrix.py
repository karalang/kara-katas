# LeetCode 766 — Toeplitz Matrix: the ★ arm in Python, same output.


def is_toeplitz_matrix(matrix):
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] != matrix[i - 1][j - 1]:
                return False
    return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(matrix):
    print(f"{matrix} -> {str(is_toeplitz_matrix(matrix)).lower()}")


def main():
    global seed
    for matrix in [[[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]], [[1, 2], [2, 2]],
                   [[7]], [[1, 2, 3]], [[1], [2], [3]], [[3, 8], [4, 3], [6, 4]],
                   [[3, 8], [4, 3], [6, 5]], [[1, 2, 3], [4, 1, 2], [5, 4, 9]]]:
        show(matrix)
    seed = 766
    yes = 0
    check = 0
    for rnd in range(300):
        m = 1 + next_random() % 20
        n = 1 + next_random() % 20
        diag = [next_random() % 4 for _ in range(m + n - 1)]
        matrix = [[diag[i - j + n - 1] for j in range(n)] for i in range(m)]
        if rnd % 2 == 1:
            i = next_random() % m
            j = next_random() % n
            matrix[i][j] = next_random() % 4
        answer = is_toeplitz_matrix(matrix)
        if answer:
            yes += 1
        check = (check * 31 + (1 if answer else 0) + rnd) % 1000000007
    print(f"300 random matrices: {yes} Toeplitz, checksum {check}")


main()
