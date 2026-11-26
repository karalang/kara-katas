# LeetCode #1476: Subrectangle Queries -- Python mirror of
# subrectangle_queries.kara: the grid kept as given, and each update
# writing its new value into every cell of the subrectangle


class SubrectangleQueries:
    def __init__(self, rectangle):
        self.rect = rectangle

    def update_subrectangle(self, row1, col1, row2, col2, new_value):
        for r in range(row1, row2 + 1):
            for c in range(col1, col2 + 1):
                self.rect[r][c] = new_value

    def get_value(self, row, col):
        return self.rect[row][col]


# ---- test harness ---------------------------------------------------------

seed = 1476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def grid(rows, cols, top):
    return [[1 + wide_random() % top for _ in range(cols)] for _ in range(rows)]


def main():
    q = SubrectangleQueries([[1, 2, 1], [4, 3, 4], [3, 2, 1], [1, 1, 1]])
    a1 = q.get_value(0, 2)
    q.update_subrectangle(0, 0, 3, 2, 5)
    a2 = q.get_value(0, 2)
    a3 = q.get_value(3, 1)
    q.update_subrectangle(3, 0, 3, 2, 10)
    a4 = q.get_value(3, 1)
    a5 = q.get_value(0, 2)
    print(f"{a1} {a2} {a3} {a4} {a5}")
    w = SubrectangleQueries([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    b1 = w.get_value(0, 0)
    w.update_subrectangle(0, 0, 2, 2, 100)
    b2 = w.get_value(0, 0)
    b3 = w.get_value(2, 2)
    w.update_subrectangle(1, 1, 2, 2, 20)
    b4 = w.get_value(2, 2)
    print(f"{b1} {b2} {b3} {b4}")
    one = SubrectangleQueries([[7]])
    c1 = one.get_value(0, 0)
    one.update_subrectangle(0, 0, 0, 0, 1000000000)
    c2 = one.get_value(0, 0)
    one.update_subrectangle(0, 0, 0, 0, 1)
    c3 = one.get_value(0, 0)
    row = SubrectangleQueries([[1, 2, 3, 4, 5]])
    row.update_subrectangle(0, 1, 0, 3, 9)
    row.update_subrectangle(0, 2, 0, 2, 8)
    r = [str(row.get_value(0, c)) for c in range(5)]
    col = SubrectangleQueries([[1], [2], [3]])
    col.update_subrectangle(1, 0, 2, 0, 6)
    k = [str(col.get_value(i, 0)) for i in range(3)]
    print(f"{c1} {c2} {c3} | {' '.join(r)} | {' '.join(k)}")
    big = SubrectangleQueries(grid(100, 100, 1000000000))
    total = 0
    for _ in range(250):
        r1 = next_random() % 100
        r2 = r1 + next_random() % (100 - r1)
        c1 = next_random() % 100
        c2 = c1 + next_random() % (100 - c1)
        v = 1 + wide_random() % 1000000000
        big.update_subrectangle(r1, c1, r2, c2, v)
        gr = next_random() % 100
        total += big.get_value(gr, next_random() % 100)
    print(f"100 by 100, 500 calls: values sum {total}")
    check = 0
    reads = 0
    for _ in range(2000):
        rows = 1 + next_random() % 10
        cols = 1 + next_random() % 10
        top = 1 + wide_random() % 1000000000
        g = SubrectangleQueries(grid(rows, cols, top))
        n = 1 + next_random() % 60
        for _ in range(n):
            if next_random() % 3 == 0:
                r1 = next_random() % rows
                r2 = r1 + next_random() % (rows - r1)
                c1 = next_random() % cols
                c2 = c1 + next_random() % (cols - c1)
                v = 1 + wide_random() % top
                g.update_subrectangle(r1, c1, r2, c2, v)
            else:
                gr = next_random() % rows
                x = g.get_value(gr, next_random() % cols)
                check = (check * 31 + x) % 1000000007
                reads += 1
    print(f"2000 random grids: {reads} reads, checksum {check}")


main()
