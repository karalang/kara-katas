# LeetCode #2133: Check if Every Row and Column Contains All Numbers --
# the benchmark, the same algorithm as valid.kara.


def check_valid(matrix):
    n = len(matrix)
    mark = [-1] * (n + 1)
    for i in range(n):
        for j in range(n):
            v = matrix[i][j]
            if mark[v] == 2 * i:
                return False
            mark[v] = 2 * i
        for j in range(n):
            v = matrix[j][i]
            if mark[v] == 2 * i + 1:
                return False
            mark[v] = 2 * i + 1
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def latin(n, seed):
    rows = list(range(n))
    symbols = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random(seed) % (i + 1)
        rows[i], rows[j] = rows[j], rows[i]
        j = next_random(seed) % (i + 1)
        symbols[i], symbols[j] = symbols[j], symbols[i]
    return [[symbols[(rows[r] + c) % n] for c in range(n)] for r in range(n)]


def main():
    seed = [2133]
    squares = [latin(100, seed) for _ in range(10)]
    valid = 0
    check = 0
    for rnd in range(20000):
        k = next_random(seed) % 10
        r = next_random(seed) % 100
        a = next_random(seed) % 100
        b = next_random(seed) % 100
        sq = squares[k]
        if rnd % 2 == 1:
            sq[a], sq[b] = sq[b], sq[a]
            ok = check_valid(sq)
        else:
            sq[r][a], sq[r][b] = sq[r][b], sq[r][a]
            ok = check_valid(sq)
            sq[r][a], sq[r][b] = sq[r][b], sq[r][a]
        x = 1 if ok else 0
        valid += x
        check = (check * 31 + x + sq[r][a]) % 1000000007
    print(f"20000 solves: {valid} valid, checksum {check}")


main()
