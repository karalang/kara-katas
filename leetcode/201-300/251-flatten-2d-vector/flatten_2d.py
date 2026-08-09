"""LeetCode 251 - Flatten 2D Vector. Python oracle.

Mirrors flatten_2d.kara algorithm-for-algorithm: the same lazy (row, col)
cursor, the same skip-past-empty-rows restoration at the top of BOTH entry
points, and the same drain harness that polls has_next twice per element and
once more after exhaustion.
"""


class Vector2D:
    def __init__(self, data):
        self.data = data
        self.row = 0
        self.col = 0

    def _skip_empty(self):
        # Python's `and` short-circuits exactly as Kara's does, so the left test
        # is the same bounds guard here.
        while self.row < len(self.data) and self.col >= len(self.data[self.row]):
            self.row += 1
            self.col = 0

    def has_next(self):
        self._skip_empty()
        return self.row < len(self.data)

    def next(self):
        self._skip_empty()
        if self.row >= len(self.data):
            return -1
        x = self.data[self.row][self.col]
        self.col += 1
        return x


def drain(v):
    out = []
    while v.has_next():
        if not v.has_next():
            return "IDEMPOTENCE BROKEN"
        out.append(str(v.next()))
    if v.has_next():
        return "EXHAUSTION BROKEN"
    return " ".join(out) if out else "(empty)"


def main():
    cases = [
        [[1, 2], [3], [4]],
        [],
        [[]],
        [[], [], []],
        [[], [1], []],
        [[], [], [7, 8], [], [], [9], []],
        [[1, 2, 3]],
    ]
    for c in cases:
        print(drain(Vector2D(c)))


if __name__ == "__main__":
    main()
