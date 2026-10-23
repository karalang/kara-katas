# LeetCode #867: Transpose Matrix -- Python mirror of the bench program
# (the ★ arm, one column at a time).

M = 1000000007


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    out = []
    for c in range(cols):
        row = []
        for r in range(rows):
            row.append(matrix[r][c])
        out.append(row)
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


def main():
    m = [[random_value() for _ in range(100)] for _ in range(1000)]
    rounds = 6000
    check = 0
    for round_ in range(rounds):
        m = transpose(m)
        r = round_ * 7 % len(m)
        c = round_ * 13 % len(m[0])
        check = (check * 31 + m[r][c] % M + M) % M
    for row in m:
        for v in row:
            check = (check * 31 + v % M + M) % M
    print(f"{rounds} transposes of a 1000 x 100 matrix: {len(m)} x {len(m[0])}, checksum {check}")


main()
