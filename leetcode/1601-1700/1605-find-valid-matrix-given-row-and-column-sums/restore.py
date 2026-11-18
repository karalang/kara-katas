# LeetCode #1605: Find Valid Matrix Given Row and Column Sums -- the
# Python mirror of restore.kara (the ★ arm): greedy, cell by cell in
# reading order. Its output is byte-identical to the Kāra arms'.


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


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def valid(m, row_sum, col_sum):
    if len(m) != len(row_sum):
        return False
    down = [0] * len(col_sum)
    for row, want in zip(m, row_sum):
        if len(row) != len(col_sum) or any(x < 0 for x in row):
            return False
        for j, x in enumerate(row):
            down[j] += x
        if sum(row) != want:
            return False
    return all(d == c for d, c in zip(down, col_sum))


def batch(count, most, top, rng):
    check = cells = ok = 0
    for _ in range(count):
        rows = rng.next() % most + 1
        cols = rng.next() % most + 1
        row_sum = [0] * rows
        col_sum = [0] * cols
        for i in range(rows):
            for j in range(cols):
                x = rng.next() % (top + 1)
                row_sum[i] += x
                col_sum[j] += x
        m = restore_matrix(row_sum, col_sum)
        if valid(m, row_sum, col_sum):
            ok += 1
        for row in m:
            for x in row:
                check = mix(check, x)
        cells += rows * cols
    print(f"{count} problems of up to {most} by {most}: {cells} cells, {ok} valid, checksum {check}")


def main():
    examples = [([3, 8], [4, 7]), ([5, 7, 10], [8, 6, 8]), ([9], [9]), ([0, 4], [1, 3]), ([6], [1, 2, 3]), ([1, 2, 3], [6])]
    for row_sum, col_sum in examples:
        m = restore_matrix(row_sum, col_sum)
        shown = ",".join("[" + ",".join(str(x) for x in row) + "]" for row in m)
        print(f"[{shown}] {'valid' if valid(m, row_sum, col_sum) else 'INVALID'}")
    rng = Rng(1605)
    batch(3000, 4, 9, rng)
    batch(300, 100, 1000, rng)
    batch(3, 500, 100000, rng)


main()
