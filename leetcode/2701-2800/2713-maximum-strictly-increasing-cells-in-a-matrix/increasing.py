# LeetCode #2713: Maximum Strictly Increasing Cells in a Matrix -- the
# Python mirror of the star arm (increasing.kara): the cells sorted by
# value, and taken a value at a time; the longest path ending at a cell
# is one more than the longest that ends anywhere in its row or column
# at a smaller value, which the row's and the column's best so far hold
# while the cells of one value are all answered before any is recorded.


def max_increasing_cells(mat):
    m = len(mat)
    n = len(mat[0])
    cells = sorted((mat[r][c], r, c) for r in range(m) for c in range(n))
    row_best = [0] * m
    col_best = [0] * n
    best = 0
    i = 0
    while i < len(cells):
        j = i
        while j < len(cells) and cells[j][0] == cells[i][0]:
            j += 1
        found = []
        for k in range(i, j):
            _, r, c = cells[k]
            found.append(max(row_best[r], col_best[c]) + 1)
        for k in range(i, j):
            _, r, c = cells[k]
            row_best[r] = max(row_best[r], found[k - i])
            col_best[c] = max(col_best[c], found[k - i])
            best = max(best, found[k - i])
        i = j
    return best


seed = 2713


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


print(max_increasing_cells([[3, 1], [3, 4]]))
print(max_increasing_cells([[1, 1], [1, 1]]))
print(max_increasing_cells([[3, 1, 6], [-9, 5, 7]]))
print(max_increasing_cells([[5]]))
print(max_increasing_cells([[r * 300 + c for c in range(300)] for r in range(300)]))
print(max_increasing_cells([[7] * 100000]))
print(max_increasing_cells([[i - 50000] for i in range(100000)][::-1]))
total = 0
check = 0
for _ in range(1000):
    m = next_random() % 8 + 1
    n = next_random() % 8 + 1
    spread = next_random() % 20 + 1
    mat = [[next_random() % spread - 10 for _ in range(n)] for _ in range(m)]
    cells = max_increasing_cells(mat)
    total += cells
    check = (check * 31 + cells) % 1000000007
print(f"1000 small matrices: cells sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(20):
    m = next_random() % 200 + 1
    n = next_random() % 200 + 1
    mat = [[wide() % 200001 - 100000 for _ in range(n)] for _ in range(m)]
    cells = max_increasing_cells(mat)
    total += cells
    check = (check * 31 + cells) % 1000000007
print(f"20 matrices up to 200 by 200: cells sum to {total}, checksum {check}")
