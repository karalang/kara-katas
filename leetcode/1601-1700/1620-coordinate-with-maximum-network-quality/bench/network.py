"""LeetCode #1620: Coordinate With Maximum Network Quality -- the bench in
Python, mirroring network.kara: every point, every tower, f64 distances."""
import math


def best_coordinate(towers, radius):
    best = [0, 0]
    most = 0
    for x in range(51):
        for y in range(51):
            quality = 0
            for t in towers:
                dx, dy = t[0] - x, t[1] - y
                d = math.sqrt(dx * dx + dy * dy)
                if d <= radius:
                    quality += math.floor(t[2] / (1.0 + d))
            if quality > most:
                most = quality
                best = [x, y]
    return best


def main():
    seed = 1620

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for _ in range(1000):
        towers = []
        for _ in range(50):
            x = next_random() % 51
            y = next_random() % 51
            q = next_random() % 51
            towers.append([x, y, q])
        radius = next_random() % 50 + 1
        cases.append((towers, radius))
    check = spread = 0
    for towers, radius in cases:
        best = best_coordinate(towers, radius)
        spread += best[0] + best[1]
        check = (check * 31 + best[0] * 51 + best[1] + 1) % 1000000007
    print(f"1000 cases of 50 towers: coordinates sum to {spread}, checksum {check}")


main()
