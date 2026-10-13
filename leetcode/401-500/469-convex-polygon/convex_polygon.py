# LeetCode #469: Convex Polygon -- the sign of every turn.
# Mirror of convex_polygon.kara (the ★ arm), with the same harness.


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


# ---- test harness ----------------------------------------------------------


def show(name, points):
    print(f"{name}: {'true' if is_convex(points) else 'false'}")


def div(a, b):
    # Kāra's integer division truncates toward zero; Python's // floors.
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


seed = 469


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def before(a, b):
    ax, ay = a
    bx, by = b
    upper_a = ay > 0 or (ay == 0 and ax > 0)
    upper_b = by > 0 or (by == 0 and bx > 0)
    if upper_a != upper_b:
        return upper_a
    return ax * by - ay * bx > 0


def random_convex(edges, size):
    vectors = []
    sx = sy = 0
    while len(vectors) < edges - 1:
        x = next_random() % (2 * size + 1) - size
        y = next_random() % (2 * size + 1) - size
        if x != 0 or y != 0:
            vectors.append((x, y))
            sx += x
            sy += y
    if sx != 0 or sy != 0:
        vectors.append((-sx, -sy))
    for i in range(1, len(vectors)):
        j = i
        while j > 0 and before(vectors[j], vectors[j - 1]):
            vectors[j], vectors[j - 1] = vectors[j - 1], vectors[j]
            j -= 1
    points = []
    x = next_random() % 100
    y = next_random() % 100
    for dx, dy in vectors:
        points.append((2 * x, 2 * y))
        x += dx
        y += dy
    return points


def area2(points):
    n = len(points)
    total = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return total


def inside(points, q):
    n = len(points)
    qx, qy = q
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if (x2 - x1) * (qy - y1) - (y2 - y1) * (qx - x1) <= 0:
            return False
    return True


def dented(points):
    n = len(points)
    cx = div(sum(x for x, _ in points), n)
    cy = div(sum(y for _, y in points), n)
    at = next_random() % n
    x1, y1 = points[at]
    x2, y2 = points[(at + 1) % n]
    mx = div(x1 + x2, 2)
    my = div(y1 + y2, 2)
    depth = 2 + next_random() % 4
    dent = (mx + div(cx - mx, depth), my + div(cy - my, depth))
    if not inside(points, dent):
        dent = (mx, my)
    out = []
    for i in range(n):
        out.append(points[i])
        if i == at:
            out.append(dent)
    return out


def main():
    show("square", [(0, 0), (0, 5), (5, 5), (5, 0)])
    show("square with a dent", [(0, 0), (0, 10), (10, 10), (10, 0), (5, 5)])
    show("triangle", [(0, 0), (4, 0), (0, 3)])
    show("triangle, other way round", [(0, 0), (0, 3), (4, 0)])
    show("points along the edges", [(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (0, 4), (0, 2)])
    show("arrow", [(0, 0), (4, 2), (0, 4), (1, 2)])
    show("hexagon", [(2, 0), (4, 0), (6, 3), (4, 6), (2, 6), (0, 3)])
    show("L shape", [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)])
    show("thin wedge", [(0, 0), (10000, 1), (10000, 2)])
    show("almost straight", [(0, 0), (5000, 1), (10000, 2), (10000, 5), (0, 5)])
    show("bent in by one", [(0, 0), (5000, 1), (10000, 0), (10000, 5), (0, 5)])
    count = 300
    convex = 0
    checksum = 0
    made = 0
    while made < count:
        edges = 3 + next_random() % 38
        size = [3, 30, 3000][next_random() % 3]
        points = random_convex(edges, size)
        if area2(points) == 0:
            continue
        if next_random() % 2 == 0:
            points = dented(points)
        made += 1
        answer = is_convex(points)
        if answer:
            convex += 1
        checksum = (checksum * 3 + (1 if answer else 2)) % 1000000007
    print(f"{count} random polygons: {convex} convex, checksum {checksum}")


main()
