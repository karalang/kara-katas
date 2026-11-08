# LeetCode #1515 bench: the ★ arm's ternary search twice, as centre.kara.
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


seed = 1515


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


check = 0
for _ in range(100):
    positions = []
    for _ in range(50):
        x = next_random() % 101
        y = next_random() % 101
        positions.append((x, y))
    answer = get_min_dist_sum(positions)
    check = (check * 31 + math.floor(answer * 100.0 + 0.5) + 1) % 1000000007
print(f"100 sets of 50 customers on 0..100: checksum {check}")
