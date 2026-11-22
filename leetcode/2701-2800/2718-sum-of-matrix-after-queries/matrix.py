# LeetCode #2718: Sum of Matrix After Queries -- the ★ arm (matrix.kara)
# in Python: the queries read from the last back, each row or column not
# set later filling the lines of the other kind not yet taken.


def matrix_sum_queries(n, queries):
    row_taken = [False] * n
    col_taken = [False] * n
    rows_left = n
    cols_left = n
    total = 0
    for kind, index, value in reversed(queries):
        if kind == 0:
            if not row_taken[index]:
                row_taken[index] = True
                rows_left -= 1
                total += value * cols_left
        elif not col_taken[index]:
            col_taken[index] = True
            cols_left -= 1
            total += value * rows_left
    return total


seed = 2718


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def random_queries(n, q, most):
    queries = []
    for _ in range(q):
        kind = next_random() % 2
        index = wide() % n
        value = wide() % (most + 1)
        queries.append([kind, index, value])
    return queries


print(matrix_sum_queries(3, [[0, 0, 1], [1, 2, 2], [0, 2, 3], [1, 0, 4]]))
print(matrix_sum_queries(3, [[0, 0, 4], [0, 1, 2], [1, 0, 1], [0, 2, 3], [1, 2, 1]]))
print(matrix_sum_queries(1, [[1, 0, 7]]))
print(matrix_sum_queries(10000, [[0, 9999, 100000]]))
sweep = [[0, i, i] for i in range(10000)] + [[1, i, 100000 - i] for i in range(10000)]
print(matrix_sum_queries(10000, sweep))
total = 0
check = 0
for _ in range(2000):
    n = next_random() % 8 + 1
    q = next_random() % 20 + 1
    s = matrix_sum_queries(n, random_queries(n, q, 10))
    total += s
    check = (check * 31 + s) % 1000000007
print(f"2000 small cases: sums sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(40):
    n = wide() % 10000 + 1
    q = wide() % 50000 + 1
    s = matrix_sum_queries(n, random_queries(n, q, 100000))
    total += s
    check = (check * 31 + s % 1000000007) % 1000000007
print(f"40 large cases: sums sum to {total}, checksum {check}")
