# Benchmark for #447: mirror of number_of_boomerangs.kara (a map of
# distances per point) on 10 random sets of 1,000 distinct points on a
# 300 x 300 grid, built once.


def number_of_boomerangs(points):
    total = 0
    for i in range(len(points)):
        counts = {}
        for j in range(len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d = dx * dx + dy * dy
            counts[d] = counts.get(d, 0) + 1
        for c in counts.values():
            total += c * (c - 1)
    return total


seed = 447


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 10
    n = 1000
    sets = []
    for _ in range(count):
        seen = set()
        points = []
        while len(points) < n:
            x = next_random() % 300
            y = next_random() % 300
            if (x, y) not in seen:
                seen.add((x, y))
                points.append((x, y))
        sets.append(points)
    total = 0
    checksum = 0
    for points in sets:
        answer = number_of_boomerangs(points)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{count} sets of {n} points: {total} boomerangs, checksum {checksum}")


main()
