# LeetCode #939: Minimum Area Rectangle -- pairs as diagonals.
# Mirrors min_area_rect.kara (the ★ arm) and prints the same output.


def min_area_rect(points):
    seen = set()
    for p in points:
        seen.add(p[0] * 40001 + p[1])
    best = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 != x2 and y1 != y2 and x1 * 40001 + y2 in seen and x2 * 40001 + y1 in seen:
                area = abs(x1 - x2) * abs(y1 - y2)
                if best == 0 or area < best:
                    best = area
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid_points(n, w, h, step, ox, oy):
    want = n if n < w * h else w * h
    taken = set()
    out = []
    while len(out) < want:
        c = (next_random() * 32768 + next_random()) % (w * h)
        if c not in taken:
            taken.add(c)
            out.append([ox + (c % w) * step, oy + (c // w) * step])
    return out


def show(points):
    return "[" + ",".join(f"[{p[0]},{p[1]}]" for p in points) + "]"


def main():
    global seed
    examples = [
        [[1, 1], [1, 3], [3, 1], [3, 3], [2, 2]],
        [[1, 1], [1, 3], [3, 1], [3, 3], [4, 1], [4, 3]],
        [[5, 5]],
        [[0, 0], [0, 2], [2, 2]],
        [[0, 7], [1, 7], [2, 7], [3, 7], [4, 7]],
        [[1, 0], [0, 1], [2, 1], [1, 2]],
        [[0, 0], [0, 40000], [40000, 0], [40000, 40000]],
        [[0, 0], [4, 0], [0, 3], [4, 3], [1, 1], [2, 1], [1, 2], [2, 2]],
    ]
    for e in examples:
        print(f"{show(e)}: {min_area_rect(e)}")
    seed = 939
    count = found = total = check = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        w = 2 + next_random() % 9
        h = 2 + next_random() % 9
        step = 1 + next_random() % 1000
        ox = next_random() % 1000
        oy = next_random() % 1000
        points = grid_points(n, w, h, step, ox, oy)
        a = min_area_rect(points)
        count += len(points)
        if a > 0:
            found += 1
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random sets of {count} points: {found} with a rectangle, areas adding to {total}, checksum {check}")
    full = grid_points(500, 25, 20, 1, 0, 0)
    print(f"a 25 by 20 grid, every point: {min_area_rect(full)}")
    spread = grid_points(500, 100, 100, 400, 0, 0)
    print(f"500 points of a 100 by 100 grid, 400 apart: {min_area_rect(spread)}")
    scattered = grid_points(500, 40001, 40001, 1, 0, 0)
    print(f"500 points anywhere: {min_area_rect(scattered)}")
    left = grid_points(250, 1, 40001, 1, 0, 0)
    sides = []
    for p in left:
        sides.append([0, p[1]])
        sides.append([40000, p[1]])
    print(f"250 heights at x = 0 and at x = 40000: {min_area_rect(sides)}")
    diagonal = [[i * 80, i * 80] for i in range(500)]
    print(f"500 points on a diagonal: {min_area_rect(diagonal)}")


main()
