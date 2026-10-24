# LeetCode #973: K Closest Points to Origin -- Python mirror of
# k_closest.kara.


def k_closest(points, k):
    s = sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])
    return s[:k]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n, span):
    points = []
    for _ in range(n):
        x = next_random() % (2 * span + 1) - span
        y = next_random() % (2 * span + 1) - span
        points.append((x, y))
    ds = sorted(x * x + y * y for x, y in points)
    ks = [k for k in range(1, n) if ds[k - 1] < ds[k]]
    ks.append(n)
    return points, ks[next_random() % len(ks)]


def show(answer):
    return "[" + ",".join(f"[{x},{y}]" for x, y in sorted(answer)) + "]"


def fold(check, answer):
    c = check
    for x, y in sorted(answer):
        c = (c * 31 + (x + 10001) * 20003 + y + 10001) % 1000000007
    return c


def main():
    global seed
    cases = [
        ([(1, 3), (-2, 2)], 1),
        ([(3, 3), (5, -1), (-2, 4)], 2),
        ([(0, 0)], 1),
        ([(1, 0), (0, 1), (-1, 0), (0, -1), (2, 2)], 4),
        ([(1, 0), (0, 1), (-1, 0), (0, -1), (2, 2)], 5),
        ([(10000, 10000), (-10000, -10000), (1, -1)], 1),
        ([(10000, -10000), (-10000, 10000), (0, 0)], 3),
        ([(3, 4), (5, 0), (0, -5), (1, 1), (6, 0)], 1),
        ([(3, 4), (5, 0), (0, -5), (1, 1), (6, 0)], 4),
        ([(2, 2), (2, 2), (1, 1), (3, 3)], 3),
    ]
    for points, k in cases:
        print(f"k = {k}: {show(k_closest(points, k))}")
    seed = 973
    for count, most, span in [(300, 12, 5), (3000, 40, 100), (4, 10000, 10000)]:
        total = check = 0
        for _ in range(count):
            n = most if most == 10000 else 1 + next_random() % most
            points, k = random_case(n, span)
            answer = k_closest(points, k)
            total += len(answer)
            check = fold(check, answer)
        print(f"{count} random cases of up to {most} points: "
              f"{total} points kept, checksum {check}")


main()
