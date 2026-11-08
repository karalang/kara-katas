# LeetCode #2013: Detect Squares -- a mirror of the ★ arm, squares.kara.


class DetectSquares:
    def __init__(self):
        self.rows = [[] for _ in range(1001)]
        self.points = []

    def at(self, x, y):
        return 0 if not self.rows[x] else self.rows[x][y]

    def add(self, point):
        x, y = point
        if not self.rows[x]:
            self.rows[x] = [0] * 1001
        if self.rows[x][y] == 0:
            self.points.append(point)
        self.rows[x][y] += 1

    def count(self, point):
        x, y = point
        ways = 0
        for px, py in self.points:
            if px != x and abs(px - x) == abs(py - y):
                ways += self.at(px, py) * self.at(x, py) * self.at(px, y)
        return ways


seed = 2013


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def run(ops, base, side, every):
    squares = DetectSquares()
    total = 0
    check = 0
    for _ in range(ops):
        x = base + next_random() % side
        point = (x, base + next_random() % side)
        if next_random() % every == 0:
            ways = squares.count(point)
            total += ways
            check = mix(check, ways)
        else:
            squares.add(point)
    return total, check


def main():
    squares = DetectSquares()
    squares.add((3, 10))
    squares.add((11, 2))
    squares.add((3, 2))
    print(f"count (11, 10) -> {squares.count((11, 10))}")
    print(f"count (14, 8) -> {squares.count((14, 8))}")
    squares.add((11, 2))
    print(f"count (11, 10) -> {squares.count((11, 10))}")
    squares.add((3, 18))
    squares.add((11, 18))
    print(f"count (3, 10) -> {squares.count((3, 10))}")
    print(f"count (3, 2) -> {squares.count((3, 2))}")
    print(f"count (19, 10) -> {squares.count((19, 10))}")
    squares.add((0, 0))
    squares.add((1000, 1000))
    squares.add((0, 1000))
    print(f"count (1000, 0) -> {squares.count((1000, 0))}")
    total = 0
    check = 0
    for _ in range(200):
        ops = next_random() % 40 + 1
        side = next_random() % 6 + 1
        every = next_random() % 4 + 2
        s, c = run(ops, next_random() % 990, side, every)
        total += s
        check = mix(check, c)
    print(f"200 runs of 1 to 40 operations: sum {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(4):
        side = [10, 20, 40, 1001][a]
        s, c = run(400, 0, side, 3)
        total += s
        check = mix(check, c)
    print(f"4 runs of 400 operations: sum {total}, checksum {check}")


main()
