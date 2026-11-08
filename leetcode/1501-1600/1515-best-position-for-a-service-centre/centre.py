# LeetCode #1515: Best Position for a Service Centre -- the Python mirror
# of the ★ arm (centre.kara): ternary search twice, 60 rounds each.
import math


def cost(positions, x, y):
    total = 0.0
    for px, py in positions:
        dx = px - x
        dy = py - y
        total += math.sqrt(dx * dx + dy * dy)
    return total


def best_on(positions, x):
    lo, hi = 0.0, 100.0
    for _ in range(60):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if cost(positions, x, m1) < cost(positions, x, m2):
            hi = m2
        else:
            lo = m1
    return cost(positions, x, (lo + hi) / 2.0)


def get_min_dist_sum(positions):
    lo, hi = 0.0, 100.0
    for _ in range(60):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if best_on(positions, m1) < best_on(positions, m2):
            hi = m2
        else:
            lo = m1
    return best_on(positions, (lo + hi) / 2.0)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, side, rng):
    check = 0
    for _ in range(count):
        n = rng.next() % most + 1
        positions = []
        for _ in range(n):
            x = rng.next() % (side + 1)
            y = rng.next() % (side + 1)
            positions.append((x, y))
        answer = get_min_dist_sum(positions)
        check = mix(check, math.floor(answer * 100.0 + 0.5))
    return check


def main():
    print(f"example 1 -> {get_min_dist_sum([(0, 1), (1, 0), (1, 2), (2, 1)]):.5f}")
    print(f"example 2 -> {get_min_dist_sum([(1, 1), (3, 3)]):.5f}")
    print(f"one customer -> {get_min_dist_sum([(5, 7)]):.5f}")
    print(f"a triangle -> {get_min_dist_sum([(0, 0), (100, 0), (50, 87)]):.5f}")
    rng = Rng(1515)
    print(f"300 sets of 1 to 8 customers on 0..10: checksum {batch(300, 8, 10, rng)}")
    print(f"30 sets of 1 to 50 customers on 0..100: checksum {batch(30, 50, 100, rng)}")


main()
