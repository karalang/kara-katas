"""Benchmark workload for LeetCode #251 — Flatten 2D Vector (Python; scale lane)."""


class Vector2D:
    def __init__(self, data):
        self.data = data
        self.row = 0
        self.col = 0

    def skip_empty(self):
        while self.row < len(self.data) and self.col >= len(self.data[self.row]):
            self.row += 1
            self.col = 0

    def has_next(self):
        self.skip_empty()
        return self.row < len(self.data)

    def next(self):
        self.skip_empty()
        if self.row >= len(self.data):
            return -1
        x = self.data[self.row][self.col]
        self.col += 1
        return x


def main():
    rows = 20000
    passes = 1500

    data = []
    state = 251251
    for _ in range(rows):
        state = (state * 1103515245 + 12345) & 2147483647
        row = []
        if (state // 65536) % 100 >= 45:
            state = (state * 1103515245 + 12345) & 2147483647
            cols = (state // 65536) % 6 + 1
            for _ in range(cols):
                state = (state * 1103515245 + 12345) & 2147483647
                row.append((state // 65536) % 1000)
        data.append(row)

    sink = 0
    for _ in range(passes):
        v = Vector2D(data)
        while v.has_next():
            x = v.next()
            sink = (sink * 31 + x + 1) % 1000000007
    print(sink)


main()
