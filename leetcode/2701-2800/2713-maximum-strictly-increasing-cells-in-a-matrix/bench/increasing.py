# LeetCode #2713: Maximum Strictly Increasing Cells in a Matrix -- the
# bench (increasing.kara in Python): the cells sorted by value, each
# value's cells answered from their row's and column's best before any is
# recorded.


def max_increasing_cells(mat):
    m, n = len(mat), len(mat[0])
    cells = [(mat[r][c], r, c) for r in range(m) for c in range(n)]
    cells.sort()
    row_best = [0] * m
    col_best = [0] * n
    best = 0
    i = 0
    while i < len(cells):
        j = i
        while j < len(cells) and cells[j][0] == cells[i][0]:
            j += 1
        found = [max(row_best[r], col_best[c]) + 1 for _, r, c in cells[i:j]]
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


count, rounds = 10, 10
mats = []
for _ in range(count):
    spread = next_random() % 9991 + 10
    mats.append([[next_random() % spread for _ in range(300)] for _ in range(300)])
total = 0
check = 0
for r in range(rounds):
    for mat in mats:
        cells = max_increasing_cells(mat)
        total += cells
        check = (check * 31 + cells + r) % 1000000007
print(f"{count} matrices of 300 by 300, {rounds} rounds: cells sum to {total}, checksum {check}")
