# LeetCode #1572: Matrix Diagonal Sum -- bench: the ★ arm (two cells a
# row, the centre taken off once) over one matrix of 1001 rows of values
# from 1 to 100, built once; then 200000 rounds, each writing one random
# cell and summing the diagonals again.


def diagonal_sum(mat):
    n = len(mat)
    total = 0
    for i in range(n):
        total += mat[i][i] + mat[i][n - 1 - i]
    if n % 2 == 1:
        total -= mat[n // 2][n // 2]
    return total


seed = 1572


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 1001
    rounds = 200000
    mat = [[next_random() % 100 + 1 for _ in range(n)] for _ in range(n)]
    check = 0
    total = 0
    for _ in range(rounds):
        r = next_random() % n
        c = next_random() % n
        mat[r][c] = next_random() % 100 + 1
        s = diagonal_sum(mat)
        total += s
        check = mix(check, s)
    print(f"{rounds} rounds on {n} rows: sums total {total}, checksum {check}")


main()
