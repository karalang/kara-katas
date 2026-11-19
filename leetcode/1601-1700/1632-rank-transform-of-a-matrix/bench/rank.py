# LeetCode #1632: Rank Transform of a Matrix -- the bench's Python mirror:
# the ★ arm on 12 random 300 x 300 matrices of values 0 to 9999, all drawn
# first.


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


seed = 1632


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    matrices = [[[next_random() % 10000 for _ in range(300)] for _ in range(300)] for _ in range(12)]
    check = 0
    total = 0
    for matrix in matrices:
        for row in matrix_rank_transform(matrix):
            for rank in row:
                total += rank
                check = (check * 31 + rank) % 1000000007
    print(f"12 matrices of 300 x 300: ranks sum to {total}, checksum {check}")


main()
