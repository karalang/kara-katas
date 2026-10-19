# LeetCode 766 — Toeplitz Matrix: benchmark, the ★ arm in Python.
# Sixteen 200 by 200 Toeplitz matrices, built once; ROUNDS rounds of
# changing one cell, asking, and putting it back.


def is_toeplitz_matrix(matrix):
    for i in range(1, len(matrix)):
        above = matrix[i - 1]
        row = matrix[i]
        for j in range(1, len(row)):
            if row[j] != above[j - 1]:
                return False
    return True


seed = 766


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 200
    rounds = 30000
    pool = []
    for _ in range(16):
        diag = [next_random() % 10 for _ in range(2 * size - 1)]
        pool.append([[diag[i - j + size - 1] for j in range(size)] for i in range(size)])
    yes = 0
    check = 0
    for rnd in range(rounds):
        k = rnd % 16
        i = next_random() % size
        j = next_random() % size
        old = pool[k][i][j]
        pool[k][i][j] = old + next_random() % 2
        answer = is_toeplitz_matrix(pool[k])
        pool[k][i][j] = old
        if answer:
            yes += 1
        check = (check * 31 + (1 if answer else 0) + i * size + j) % 1000000007
    print(f"{rounds} rounds on 200 by 200: {yes} Toeplitz, checksum {check}")


main()
