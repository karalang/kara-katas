# LeetCode #2013: Detect Squares -- the ★ arm's benchmark, a mirror of
# squares.kara.


class DetectSquares:
    def __init__(self):
        self.rows = [[] for _ in range(1001)]
        self.points = []

    def at(self, x, y):
        row = self.rows[x]
        return row[y] if row else 0

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


def main():
    calls = total = check = 0
    for r in range(20):
        squares = DetectSquares()
        for _ in range(20000):
            base = (r % 10) * 90
            point = (base + next_random() % 60, base + next_random() % 60)
            if next_random() % 3 == 0:
                ways = squares.count(point)
                calls += 1
                total += ways
                check = (check * 31 + ways) % 1000000007
            else:
                squares.add(point)
    print(f"{calls} counts: sum {total}, checksum {check}")


main()
