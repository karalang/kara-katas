# LeetCode #1575: Count All Possible Routes -- bench: the ★ arm (routes to
# the finish filled from no fuel up) over 100 problems of 60 distinct
# locations below 300 and a fuel of 200, every problem drawn first.


def count_routes(locations, start, finish, fuel):
    m = 1000000007
    n = len(locations)
    ways = [[0] * n for _ in range(fuel + 1)]
    for f in range(fuel + 1):
        for c in range(n):
            total = 1 if c == finish else 0
            for d in range(n):
                cost = abs(locations[c] - locations[d])
                if d != c and cost <= f:
                    total = (total + ways[f - cost][d]) % m
            ways[f][c] = total
    return ways[fuel][start]


seed = 1575


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 60
    problems = []
    for _ in range(100):
        locations = []
        while len(locations) < n:
            x = next_random() % 300
            if x not in locations:
                locations.append(x)
        start = next_random() % n
        finish = next_random() % n
        problems.append((locations, start, finish))
    check = 0
    total = 0
    for locations, start, finish in problems:
        routes = count_routes(locations, start, finish, 200)
        total += routes
        check = mix(check, routes)
    print(f"100 problems of {n} locations and fuel 200: routes total {total}, checksum {check}")


main()
