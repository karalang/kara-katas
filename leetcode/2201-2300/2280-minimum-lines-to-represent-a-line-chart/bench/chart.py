# LeetCode #2280: Minimum Lines to Represent a Line Chart -- the bench,
# the ★ arm.


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


# ---- bench harness ---------------------------------------------------------

seed = 2280


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(20):
        points = []
        day = 1
        price = 500000000
        while len(points) < 100000:
            dx = next_random() % 1000 + 1
            dy = next_random() % 2001 - 1000
            run = next_random() % 5 + 1
            for _ in range(run):
                if len(points) < 100000:
                    points.append([day, price])
                    day += dx
                    price += dy
        for i in range(99999, 0, -1):
            high = next_random()
            j = (high * 32768 + next_random()) % (i + 1)
            points[i], points[j] = points[j], points[i]
        check = (check * 31 + minimum_lines(points)) % 1000000007
    print(f"20 charts of 10^5: checksum {check}")


main()
