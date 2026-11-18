# LeetCode #2280: Minimum Lines to Represent a Line Chart -- the Python
# mirror of the ★ arm, `chart.kara`.


def minimum_lines(stock_prices):
    points = sorted(stock_prices, key=lambda p: p[0])
    n = len(points)
    if n < 2:
        return 0
    lines = 1
    for i in range(2, n):
        a, b, c = points[i - 2], points[i - 1], points[i]
        if (b[1] - a[1]) * (c[0] - b[0]) != (c[1] - b[1]) * (b[0] - a[0]):
            lines += 1
    return lines


# ---- test harness ---------------------------------------------------------

seed = 2280


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def chart(n, step, base):
    points = []
    day = next_random() % 10 + 1
    price = base
    while len(points) < n:
        dx = wide_random() % step + 1
        dy = wide_random() % (2 * step + 1) - step
        run = next_random() % 5 + 1
        for _ in range(run):
            if len(points) < n:
                points.append([day, price])
                day += dx
                price += dy
    for i in range(len(points) - 1, 0, -1):
        j = next_random() % (i + 1)
        points[i], points[j] = points[j], points[i]
    return points


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    examples = [
        [[1, 7], [2, 6], [3, 5], [4, 4], [5, 4], [6, 3], [7, 2], [8, 1]],
        [[3, 4], [1, 2], [7, 8], [2, 3]],
        [[5, 5]],
        [[1, 1], [1000000000, 1000000000]],
        [[1, 1], [2, 2], [3, 1]],
        [[4, 2], [1, 1], [3, 1], [2, 2], [5, 1]],
        [[1, 1], [500000000, 499999999], [1000000000, 999999998]],
    ]
    for points in examples:
        print(f"{show(points)} -> {minimum_lines(points)}")
    check = 0
    for t in range(2000):
        n = next_random() % 40 + 1
        stock_prices = chart(n, [2, 30, 1000000][t % 3], [100, 2000, 100000000][t % 3])
        check = (check * 31 + minimum_lines(stock_prices)) % 1000000007
    print(f"2000 charts: checksum {check}")
    walked = chart(100000, 1000, 500000000)
    line = [[i * 9999, 3 * i + 7] for i in range(1, 100001)]
    zigzag = [[i, i % 2 + 1] for i in range(1, 100001)]
    answers = [minimum_lines(walked), minimum_lines(line), minimum_lines(zigzag)]
    print(f"10^5 points: {show(answers)}")


main()
