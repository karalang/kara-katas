# LeetCode #1575: Count All Possible Routes -- the Python mirror of the ★
# arm: ways[f][c], the routes from city c with f fuel left that end at the
# finish, is 1 for standing at the finish plus the routes after each move
# it can afford, filled from no fuel up. O(fuel * n^2)


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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, spread, tank):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        taken = set()
        locations = []
        while len(locations) < n:
            x = (next_random() * 32768 + next_random()) % spread
            if x not in taken:
                taken.add(x)
                locations.append(x)
        start = next_random() % n
        finish = next_random() % n
        fuel = next_random() % tank + 1
        routes = count_routes(locations, start, finish, fuel)
        total += routes
        check = mix(check, routes)
    print(f"{count} problems of up to {most} locations: routes total {total}, checksum {check}")


def main():
    global seed
    examples = [
        ([2, 3, 6, 8, 4], 1, 3, 5),
        ([4, 3, 1], 1, 0, 6),
        ([5, 2, 1], 0, 2, 3),
        ([1, 2], 0, 0, 1),
        ([1, 2], 0, 0, 2),
        ([1, 2, 3], 1, 1, 200),
    ]
    for locations, start, finish, fuel in examples:
        print(f"{locations}, start {start}, finish {finish}, fuel {fuel} -> {count_routes(locations, start, finish, fuel)}")
    seed = 1575
    batch(3000, 5, 10, 8)
    batch(300, 20, 100, 60)
    batch(10, 100, 1000000000, 200)
    batch(10, 100, 200, 200)


main()
