# LeetCode #1605: Find Valid Matrix Given Row and Column Sums -- the bench
# in Python, mirroring restore.kara: greedy, cell by cell in reading order.


def restore_matrix(row_sum, col_sum):
    rows, cols = list(row_sum), list(col_sum)
    m = []
    for i in range(len(rows)):
        row = [0] * len(cols)
        for j in range(len(cols)):
            x = min(rows[i], cols[j])
            row[j] = x
            rows[i] -= x
            cols[j] -= x
        m.append(row)
    return m


def main():
    seed = 1605

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(100):
        row_sum = [0] * 1000
        col_sum = [0] * 1000
        for i in range(1000):
            for j in range(1000):
                x = next_random() % 1001
                row_sum[i] += x
                col_sum[j] += x
        problems.append((row_sum, col_sum))
    check = nonzero = 0
    for row_sum, col_sum in problems:
        for row in restore_matrix(row_sum, col_sum):
            for x in row:
                if x != 0:
                    nonzero += 1
                    check = (check * 31 + x + 1) % 1000000007
    print(f"100 problems of 1000 by 1000: {nonzero} cells not zero, checksum {check}")


main()
