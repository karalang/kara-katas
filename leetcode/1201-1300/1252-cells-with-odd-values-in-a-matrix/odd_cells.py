# LeetCode #1252: Cells with Odd Values in a Matrix -- the Python mirror
# of odd_cells.kara: the matrix itself, every cell of each place's row
# and column raised by one, then the odd cells counted.


def odd_cells(m, n, indices):
    matrix = [[0] * n for _ in range(m)]
    for r, c in indices:
        for j in range(n):
            matrix[r][j] += 1
        for i in range(m):
            matrix[i][c] += 1
    return sum(1 for row in matrix for v in row if v % 2 == 1)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_indices(m, n, k):
    out = []
    for _ in range(k):
        r = next_random() % m
        c = next_random() % n
        out.append([r, c])
    return out


def main():
    global seed
    print(odd_cells(2, 3, [[0, 1], [1, 1]]), odd_cells(2, 2, [[1, 1], [0, 0]]))
    seed = 1252
    total = 0
    check = 0
    for _ in range(1000):
        m = next_random() % 50 + 1
        n = next_random() % 50 + 1
        k = next_random() % 100 + 1
        odd = odd_cells(m, n, random_indices(m, n, k))
        total += odd
        check = (check * 131 + odd) % 1000000007
    print(f"1000 random matrices: total {total}, checksum {check}")
    corner = [[0, 0]] * 99
    stripes = [[i % 50, i % 37] for i in range(100)]
    edges = [[0, i] if i < 50 else [i - 50, 0] for i in range(99)]
    print(f"50 by 50: corner {odd_cells(50, 50, corner)}, stripes {odd_cells(50, 50, stripes)}, edges {odd_cells(50, 50, edges)}")


main()
