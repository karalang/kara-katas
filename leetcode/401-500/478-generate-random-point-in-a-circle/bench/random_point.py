# Benchmark for #478: Python mirror of the ★ arm (darts at the square);
# see random_point.kara.


class Uniform:
    def __init__(self, seed):
        self.seed = seed

    def step(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def next(self):
        high = self.step()
        low = self.step()
        return (high * 32768 + low) / 1073741824.0


class Solution:
    def __init__(self, radius, x_center, y_center, seed):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        self.rng = Uniform(seed)

    def rand_point(self):
        while True:
            x = 2.0 * self.rng.next() - 1.0
            y = 2.0 * self.rng.next() - 1.0
            if x * x + y * y <= 1.0:
                return (self.x_center + self.radius * x, self.y_center + self.radius * y)


def main():
    n = 20000000
    solution = Solution(10000.0, 20000.0, 30000.0, 478)
    right = 0
    checksum = 0
    for _ in range(n):
        x, y = solution.rand_point()
        if x > 20000.0:
            right += 1
        checksum = (checksum * 31 + int(x * 1000.0) + int(y * 1000.0)) % 1000000007
    print(f"{n} points: {right} right of the centre, checksum {checksum}")


main()
