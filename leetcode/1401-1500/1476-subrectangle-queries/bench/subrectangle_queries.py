# LeetCode #1476: Subrectangle Queries -- bench, Python mirror of
# subrectangle_queries.kara


class SubrectangleQueries:
    def __init__(self, rectangle):
        self.rect = rectangle

    def update_subrectangle(self, row1, col1, row2, col2, new_value):
        for r in range(row1, row2 + 1):
            row = self.rect[r]
            for c in range(col1, col2 + 1):
                row[c] = new_value

    def get_value(self, row, col):
        return self.rect[row][col]


seed = 1476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rect = []
    for _ in range(100):
        row = []
        for _ in range(100):
            hi = next_random()
            row.append(1 + (hi * 32768 + next_random()) % 1000000000)
        rect.append(row)
    q = SubrectangleQueries(rect)
    check = 0
    for p in range(5000):
        for _ in range(250):
            r1 = next_random() % 100
            r2 = r1 + next_random() % (100 - r1)
            c1 = next_random() % 100
            c2 = c1 + next_random() % (100 - c1)
            q.update_subrectangle(r1, c1, r2, c2, 1 + check % 1000000000)
            r = next_random() % 100
            c = next_random() % 100
            check = (check * 31 + q.get_value(r, c) + p) % 1000000007
    print(f"5000 passes of 250 updates on 100 by 100: checksum {check}")


main()
