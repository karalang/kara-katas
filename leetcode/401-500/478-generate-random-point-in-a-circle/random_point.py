# LeetCode #478: Generate Random Point in a Circle -- Python mirror of the
# ★ arm (random_point.kara): darts at the square, kept when inside.
import math


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


def even(counts, n, sds):
    p = 1.0 / len(counts)
    expect = n * p
    sd = math.sqrt(n * p * (1.0 - p))
    return all(abs(count - expect) <= sds * sd for count in counts)


def sector(u, v):
    if u >= 0.0:
        quadrant = 0 if v >= 0.0 else 3
    else:
        quadrant = 1 if v >= 0.0 else 2
    half = 0 if abs(v) < abs(u) else 1
    return quadrant * 2 + half


def ring(u, v):
    return min(int((u * u + v * v) * 10.0), 9)


def b(x):
    return "true" if x else "false"


def check(radius, x_center, y_center, seed):
    n = 100000
    solution = Solution(radius, x_center, y_center, seed)
    tolerance = 1e-9 * radius + 1e-15 * (abs(x_center) + abs(y_center))
    inside = True
    quadrants = [0] * 4
    sectors = [0] * 8
    rings = [0] * 10
    grid = [0] * 80
    sum_u = 0.0
    sum_v = 0.0
    for _ in range(n):
        x, y = solution.rand_point()
        dx = x - x_center
        dy = y - y_center
        if math.sqrt(dx * dx + dy * dy) > radius + tolerance:
            inside = False
        u = dx / radius
        v = dy / radius
        s = sector(u, v)
        r = ring(u, v)
        quadrants[s // 2] += 1
        sectors[s] += 1
        rings[r] += 1
        grid[r * 8 + s] += 1
        sum_u += u
        sum_v += v
    limit = 4.0 * math.sqrt(0.25 / n)
    centred = abs(sum_u / n) <= limit and abs(sum_v / n) <= limit
    print(f"radius {radius} at ({x_center}, {y_center}): {n} points, inside {b(inside)}, "
          f"quadrants {b(even(quadrants, n, 4.0))}, sectors {b(even(sectors, n, 4.0))}, "
          f"rings {b(even(rings, n, 4.0))}, grid {b(even(grid, n, 5.0))}, centred {b(centred)}")


def main():
    check(1.0, 0.0, 0.0, 478)
    check(10.0, 5.0, -7.5, 4781)
    check(0.01, -73839.0, 9500000.0, 4782)
    check(100000000.0, 10000000.0, -10000000.0, 4783)
    check(0.5, 0.25, 0.25, 4784)
    a = Solution(2.0, 1.0, 1.0, 7)
    bb = Solution(2.0, 1.0, 1.0, 7)
    c = Solution(2.0, 1.0, 1.0, 8)
    same = True
    differs = False
    for _ in range(1000):
        p = a.rand_point()
        q = bb.rand_point()
        r = c.rand_point()
        if p != q:
            same = False
        if p != r:
            differs = True
    print(f"1000 points from one seed twice: same {b(same)}; from another seed: different {b(differs)}")


main()
