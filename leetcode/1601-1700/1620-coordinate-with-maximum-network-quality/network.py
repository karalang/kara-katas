"""LeetCode #1620: Coordinate With Maximum Network Quality -- Python mirror of
the ★ arm (network.kara): every point of the square, the first best."""
import math


def best_coordinate(towers, radius):
    best = [0, 0]
    most = 0
    for x in range(51):
        for y in range(51):
            quality = 0
            for tx, ty, q in towers:
                d = math.sqrt((tx - x) ** 2 + (ty - y) ** 2)
                if d <= radius:
                    quality += math.floor(q / (1.0 + d))
            if quality > most:
                most = quality
                best = [x, y]
    return best


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(towers, radius):
    return "[" + ",".join(f"[{t[0]},{t[1]},{t[2]}]" for t in towers) + f"] r={radius}"


def batch(count, most, span, rng):
    check = origin = 0
    for _ in range(count):
        n = rng.next() % most + 1
        towers = []
        for _ in range(n):
            x = rng.next() % span
            y = rng.next() % span
            q = rng.next() % 51
            towers.append([x, y, q])
        radius = rng.next() % 50 + 1
        best = best_coordinate(towers, radius)
        if best == [0, 0]:
            origin += 1
        check = mix(check, best[0] * 51 + best[1])
    print(f"{count} cases of up to {most} towers in a {span} square: {origin} at the origin, checksum {check}")


def main():
    examples = [
        ([[1, 2, 5], [2, 1, 7], [3, 1, 9]], 2),
        ([[23, 11, 21]], 9),
        ([[1, 2, 13], [2, 1, 7], [0, 1, 9]], 2),
        ([[5, 5, 1], [9, 9, 1]], 3),
        ([[3, 4, 0], [7, 7, 0]], 10),
    ]
    for towers, radius in examples:
        best = best_coordinate(towers, radius)
        print(f"{show(towers, radius)}: [{best[0]},{best[1]}]")
    rng = Rng(1620)
    batch(3000, 4, 8, rng)
    batch(300, 20, 51, rng)
    batch(30, 50, 51, rng)


main()
