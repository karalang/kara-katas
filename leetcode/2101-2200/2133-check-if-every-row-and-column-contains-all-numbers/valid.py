# LeetCode #2133: Check if Every Row and Column Contains All Numbers --
# the mirror of valid.kara: one table of marks for all 2n lines, a value
# seen twice in a line when its mark is that line's number.


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


def text(m):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in m) + "]"


def show(matrix):
    print(f"{text(matrix)} -> {str(check_valid(matrix)).lower()}")


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
    show([[1, 2, 3], [3, 1, 2], [2, 3, 1]])
    show([[1, 1, 1], [1, 2, 3], [1, 2, 3]])
    show([[1]])
    show([[1, 2], [2, 1]])
    show([[1, 2], [1, 2]])
    show([[1, 1], [2, 2]])
    seed = [2133]
    valid = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 6 + 1
        if rnd % 3 == 0:
            matrix = [[next_random(seed) % n + 1 for _ in range(n)] for _ in range(n)]
        else:
            matrix = latin(n, seed)
            if rnd % 3 == 2:
                r = next_random(seed) % n
                c = next_random(seed) % n
                matrix[r][c] = next_random(seed) % n + 1
        ok = check_valid(matrix)
        if ok:
            valid += 1
        check = (check * 31 + (1 if ok else 0) + n * 2) % 1000000007
    print(f"2000 matrices: {valid} valid, checksum {check}")
    square = latin(100, seed)
    swapped = [row[:] for row in square]
    swapped[37][10], swapped[37][90] = swapped[37][90], swapped[37][10]
    same = [list(range(1, 101)) for _ in range(100)]
    x = str(check_valid(square)).lower()
    y = str(check_valid(swapped)).lower()
    z = str(check_valid(same)).lower()
    print(f"order 100: {x} square, {y} swapped, {z} every row the same")


main()
