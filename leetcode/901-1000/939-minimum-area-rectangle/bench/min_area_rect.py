# Benchmark: LeetCode #939 Minimum Area Rectangle -- the ★ arm, pairs as
# diagonals, on 20 sets of 500 points, LeetCode's most, in 10 rounds.
# Mirrors min_area_rect.kara, .c, .rs and go-seq/.


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


seed = 939


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 10
    count = 20
    sets = []
    for _ in range(count):
        step = 1 + next_random() % 100
        ox = next_random() % 1000
        oy = next_random() % 1000
        taken = [False] * 1600
        points = []
        while len(points) < 500:
            c = (next_random() * 32768 + next_random()) % 1600
            if not taken[c]:
                taken[c] = True
                points.append([ox + (c % 40) * step, oy + (c // 40) * step])
        sets.append(points)
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            a = min_area_rect(sets[(r + i) % count])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} sets of 500 points: areas adding to {total}, checksum {check}")


main()
