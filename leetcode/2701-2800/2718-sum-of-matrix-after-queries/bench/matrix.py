# LeetCode #2718: Sum of Matrix After Queries -- the bench (matrix.kara in
# Python): the queries read from the last back, each row or column not
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
    a = next_random()
    return a * 32768 + next_random()


count, rounds = 40, 20
problems = []
for _ in range(count):
    n = 10000
    queries = []
    for _ in range(50000):
        kind = next_random() % 2
        index = wide() % n
        value = wide() % 100001
        queries.append([kind, index, value])
    problems.append((n, queries))
total = 0
check = 0
for r in range(rounds):
    for n, queries in problems:
        s = matrix_sum_queries(n, queries)
        total += s % 1000000007
        check = (check * 31 + s % 1000000007 + r) % 1000000007
print(f"{count} cases of 50000 queries on 10000 rows, {rounds} rounds: sums mod p sum to {total}, checksum {check}")
