# LeetCode #2152: Minimum Number of Lines to Cover Points -- the Python
# mirror of lines.kara's ★ arm.


def minimum_lines(points):
    n = len(points)
    full = (1 << n) - 1
    fewest = [n + 1] * (1 << n)
    fewest[0] = 0
    for mask in range(full):
        if fewest[mask] > n:
            continue
        i = 0
        while (mask >> i) & 1 == 1:
            i += 1
        alone = mask | (1 << i)
        fewest[alone] = min(fewest[alone], fewest[mask] + 1)
        for j in range(i + 1, n):
            line = 0
            for k in range(n):
                cross = (points[j][0] - points[i][0]) * (points[k][1] - points[i][1]) - (points[j][1] - points[i][1]) * (points[k][0] - points[i][0])
                if cross == 0:
                    line |= 1 << k
            fewest[mask | line] = min(fewest[mask | line], fewest[mask] + 1)
    return fewest[full]


seed = 2152


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, reach):
    points = []
    while len(points) < n:
        x = next_random() % (2 * reach + 1) - reach
        y = next_random() % (2 * reach + 1) - reach
        if [x, y] not in points:
            points.append([x, y])
    return points


def fmt(points):
    return "[" + ", ".join(f"[{x}, {y}]" for x, y in points) + "]"


def show(points):
    print(f"{fmt(points)} -> {minimum_lines(points)}")


def main():
    show([[0, 1], [2, 3], [4, 5], [4, 3]])
    show([[0, 2], [-2, -2], [1, 4]])
    show([[5, -5]])
    show([[0, 0], [100, -100]])
    show([[0, 0], [0, 1], [1, 0], [1, 1]])
    show([[k // 3, k % 3] for k in range(9)])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 8 + 1
        points = draw(n, [2, 100][rnd % 2])
        lines = minimum_lines(points)
        total += lines
        check = (check * 31 + lines + n) % 1000000007
    print(f"2000 sets: {total} lines in all, checksum {check}")
    one = [[3 * k - 14, 100 - 7 * k] for k in range(10)]
    two = [[k, k] if k < 5 else [k, -k] for k in range(10)]
    rand = draw(10, 100)
    print(f"10 points: {minimum_lines(one)} on one line, {minimum_lines(two)} on two, {minimum_lines(rand)} at random")


main()
