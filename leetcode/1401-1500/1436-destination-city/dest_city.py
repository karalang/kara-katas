# LeetCode #1436: Destination City -- the Python mirror of dest_city.kara:
# every city a path leaves from, and the one city a path reaches that no
# path leaves


def dest_city(paths):
    starts = {p[0] for p in paths}
    return next(p[1] for p in paths if p[1] not in starts)


# ---- test harness ---------------------------------------------------------

seed = 1436


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def trip(n, longest, k):
    cities = []
    while len(cities) < n + 1:
        length = 1 + next_random() % longest
        name = "".join(chr(ord('A') + next_random() % k) for _ in range(length))
        if name not in cities:
            cities.append(name)
    paths = [[cities[i], cities[i + 1]] for i in range(n)]
    for i in range(len(paths) - 1, 0, -1):
        j = next_random() % (i + 1)
        paths[i], paths[j] = paths[j], paths[i]
    return paths


def folded(name):
    h = 0
    for b in name.encode():
        h = (h * 31 + b) % 1000000007
    return h


def main():
    cases = [
        [["London", "New York"], ["New York", "Lima"], ["Lima", "Sao Paulo"]],
        [["B", "C"], ["D", "B"], ["C", "A"]],
        [["A", "Z"]],
        [["pqrs", "pq"], ["p", "pqrs"]],
    ]
    print(",".join(dest_city(p) for p in cases))
    long = trip(100, 10, 26)
    two = trip(100, 10, 2)
    print(f"100 paths: {dest_city(long)} {dest_city(two)}")
    check = 0
    letters = 0
    for _ in range(2000):
        longest = 1 + next_random() % 10
        k = 2 + next_random() % 25
        names = 0
        power = 1
        for _ in range(longest):
            power = min(power * k, 1000)
            names = min(names + power, 1000)
        n = 1 + next_random() % min(names - 1, 100)
        got = dest_city(trip(n, longest, k))
        letters += len(got)
        check = (check * 131 + folded(got)) % 1000000007
    print(f"2000 random trips: {letters} letters, checksum {check}")


main()
