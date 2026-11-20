# LeetCode #1277 bench, in Python: the ★ arm (dynamic programming over the
# sides of the largest squares) on 40 random 300-by-300 matrices, half,
# four fifths, nineteen twentieths and 99 in 100 ones, drawn once; 50
# rounds, every count folded into a checksum.


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


seed = 1277


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    percents = [50, 80, 95, 99]
    matrices = []
    for k in range(40):
        matrices.append([[1 if next_random() % 100 < percents[k % 4] else 0 for _ in range(300)] for _ in range(300)])
    check = 0
    for rnd in range(50):
        for matrix in matrices:
            check = (check * 131 + count_squares(matrix) + rnd) % 1000000007
    print(f"50 rounds of 40 matrices of 300 by 300: checksum {check}")


main()
