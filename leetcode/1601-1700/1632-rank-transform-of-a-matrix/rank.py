# LeetCode #1632: Rank Transform of a Matrix -- the Python mirror of the
# ★ arm: cells in order of value, a union-find over each value's cells
# by row and column, each group one more than its rows' and columns'
# largest rank so far.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def matrix_rank_transform(matrix):
    rows, cols = len(matrix), len(matrix[0])
    cells = sorted((matrix[r][c], r, c) for r in range(rows) for c in range(cols))
    row_max = [0] * rows
    col_max = [0] * cols
    answer = [[0] * cols for _ in range(rows)]
    parent = list(range(rows * cols))
    start = 0
    while start < len(cells):
        end = start
        while end < len(cells) and cells[end][0] == cells[start][0]:
            end += 1
        first_in_row = {}
        first_in_col = {}
        for _, r, c in cells[start:end]:
            cell = r * cols + c
            if r in first_in_row:
                a, b = find(parent, cell), find(parent, first_in_row[r])
                parent[a] = b
            else:
                first_in_row[r] = cell
            if c in first_in_col:
                a, b = find(parent, cell), find(parent, first_in_col[c])
                parent[a] = b
            else:
                first_in_col[c] = cell
        group_rank = {}
        for _, r, c in cells[start:end]:
            root = find(parent, r * cols + c)
            rank = max(row_max[r], col_max[c]) + 1
            group_rank[root] = max(group_rank.get(root, 0), rank)
        for _, r, c in cells[start:end]:
            rank = group_rank[find(parent, r * cols + c)]
            answer[r][c] = rank
            row_max[r] = rank
            col_max[c] = rank
        start = end
    return answer


# ---- the harness: the same as every arm's ---------------------------------


class Seed:
    def __init__(self, value):
        self.value = value

    def next(self):
        self.value = (self.value * 1103515245 + 12345) % 2147483648
        return self.value // 65536


def batch(count, most, spread, seed):
    check = 0
    total = 0
    for _ in range(count):
        rows = seed.next() % most + 1
        cols = seed.next() % most + 1
        matrix = [[seed.next() % (2 * spread + 1) - spread for _ in range(cols)] for _ in range(rows)]
        for row in matrix_rank_transform(matrix):
            for rank in row:
                total += rank
                check = (check * 31 + rank) % 1000000007
    print(f"{count} matrices of up to {most} x {most}: ranks sum to {total}, checksum {check}")


def show(m):
    print("[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in m) + "]")


def main():
    show(matrix_rank_transform([[1, 2], [3, 4]]))
    show(matrix_rank_transform([[7, 7], [7, 7]]))
    show(matrix_rank_transform([[20, -21, 14], [-19, 4, 19], [22, -47, 24], [-19, 4, 19]]))
    show(matrix_rank_transform([[7, 3, 6], [1, 4, 5], [9, 8, 2]]))
    show(matrix_rank_transform([[-5]]))
    show(matrix_rank_transform([[3], [3], [3]]))
    seed = Seed(1632)
    batch(2000, 4, 3, seed)
    batch(200, 30, 1000, seed)
    batch(5, 200, 5, seed)


main()
