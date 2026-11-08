# LeetCode #1074: Number of Submatrices That Sum to Target -- the Python
# mirror of submatrix_sum.kara (the ★ arm): for each pair of rows, the
# columns' sums between them read left to right as a running total, and a
# map of the totals seen so far counting the earlier ones `target` below.


def num_submatrix_sum_target(matrix, target):
    m, n = len(matrix), len(matrix[0])
    count = 0
    for top in range(m):
        column = [0] * n
        for bottom in range(top, m):
            for c in range(n):
                column[c] += matrix[bottom][c]
            seen = {0: 1}
            total = 0
            for c in range(n):
                total += column[c]
                count += seen.get(total - target, 0)
                seen[total] = seen.get(total, 0) + 1
    return count


seed = 1074


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_matrix(rows, cols, spread):
    m = next_random() % rows + 1
    n = next_random() % cols + 1
    return [[next_random() % (2 * spread + 1) - spread for _ in range(n)] for _ in range(m)]


def main():
    examples = [
        ([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 0),
        ([[1, -1], [-1, 1]], 0),
        ([[904]], 0),
        ([[5]], 5),
        ([[1, 2], [3, 4]], 10),
        ([[1, 1, 1], [1, 1, 1]], 2),
        ([[-1, 1, -1], [1, -1, 1], [-1, 1, -1]], 0),
        ([[2, -2, 2, -2]], 0),
        ([[1000], [-1000], [1000]], 1000),
    ]
    for matrix, target in examples:
        rows = " ".join(",".join(str(v) for v in row) for row in matrix)
        print(f"{rows} target {target} -> {num_submatrix_sum_target(matrix, target)}")
    for count, size, spread, label in [(3000, 5, 2, "3000 matrices up to 5 by 5"), (20, 30, 3, "20 matrices up to 30 by 30")]:
        total = check = 0
        for _ in range(count):
            matrix = random_matrix(size, size, spread)
            target = next_random() % (2 * spread + 1) - spread
            x = num_submatrix_sum_target(matrix, target)
            total += x
            check = (check * 31 + x) % 1000000007
        print(f"{label}: answers sum {total}, checksum {check}")
    zeros = [[0] * 30 for _ in range(30)]
    ones = [[1] * 30 for _ in range(30)]
    signs = [[1 if (r + c) % 2 == 0 else -1 for c in range(30)] for r in range(30)]
    wide = [[1000 if c % 2 == 0 else -1000 for c in range(100)]]
    print(f"30 by 30 of zeros, target 0: {num_submatrix_sum_target(zeros, 0)}")
    print(f"30 by 30 of ones, target 1: {num_submatrix_sum_target(ones, 1)}")
    print(f"30 by 30 of ones, target 30: {num_submatrix_sum_target(ones, 30)}")
    print(f"30 by 30 of alternating signs, target 0: {num_submatrix_sum_target(signs, 0)}")
    print(f"1 by 100 of 1000 and -1000, target 1000: {num_submatrix_sum_target(wide, 1000)}")


main()
