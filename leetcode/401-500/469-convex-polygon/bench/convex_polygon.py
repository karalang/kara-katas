# Benchmark for #469: mirror of convex_polygon.kara (the ★ arm: the sign
# of every turn) on the same workload.


def is_convex(points):
    n = len(points)
    sign = 0
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        x2, y2 = points[(i + 2) % n]
        cross = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)
        if cross != 0:
            s = 1 if cross > 0 else -1
            if sign == 0:
                sign = s
            elif s != sign:
                return False
    return True


seed = 469


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def polygon(n, dent):
    points = []
    x = -(n * 2)
    for _ in range(n):
        points.append((x, x * x))
        x += 1 + next_random() % 3
    if dent:
        i = 1 + next_random() % (n - 2)
        xa, _ = points[i - 1]
        xb, yb = points[i]
        xc, _ = points[i + 1]
        points[i] = (xb, yb + (xb - xa) * (xc - xb) + 1)
    return points


def main():
    count = 100
    n = 50000
    rounds = 20
    polygons = [polygon(n, k % 2 == 1) for k in range(count)]
    convex = 0
    checksum = 0
    for r in range(rounds):
        for k in range(count):
            answer = is_convex(polygons[k])
            if answer:
                convex += 1
            checksum = (checksum * 3 + (1 if answer else 2) + r) % 1000000007
    print(f"{rounds} rounds on {count} polygons of {n} vertices: {convex} convex, checksum {checksum}")


main()
