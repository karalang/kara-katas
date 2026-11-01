# LeetCode #1037: Valid Boomerang -- bench
# Mirrors ../boomerang.kara; see ../README.md § Benchmarks.


def is_boomerang(points):
    (ax, ay), (bx, by), (cx, cy) = points[0], points[1], points[2]
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) != 0


seed = 1037


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 1000000, 100
    triples = []
    for i in range(count):
        if i % 3 == 0:
            x, y = next_random() % 34, next_random() % 34
            dx, dy = next_random() % 34, next_random() % 34
            triples.append([(x, y), (x + dx, y + dy), (x + 2 * dx, y + 2 * dy)])
        else:
            points = []
            for _ in range(3):
                px = next_random() % 101
                py = next_random() % 101
                points.append((px, py))
            triples.append(points)
    boomerangs = 0
    check = 0
    for _ in range(rounds):
        for points in triples:
            answer = is_boomerang(points)
            if answer:
                boomerangs += 1
            check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"{count} triples, {rounds} rounds: {boomerangs} boomerangs, checksum {check}")


main()
