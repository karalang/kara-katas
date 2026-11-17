# LeetCode #1182: Shortest Distance to Target Color -- mirror of the ★ arm
# (a nearest-distance table per colour, a sweep from each side). Every answer
# is also checked against the statement read literally: the least |i - j|
# over every j holding the colour, or -1 when none does.


def shortest_distance_color(colors, queries):
    n = len(colors)
    far = n + 1
    nearest = []
    for c in range(1, 4):
        dist = [far] * n
        last = -1
        for i in range(n):
            if colors[i] == c:
                last = i
            if last >= 0:
                dist[i] = i - last
        last = -1
        for i in range(n - 1, -1, -1):
            if colors[i] == c:
                last = i
            if last >= 0 and last - i < dist[i]:
                dist[i] = last - i
        nearest.append(dist)
    answer = []
    for i, c in queries:
        d = nearest[c - 1][i]
        answer.append(-1 if d == far else d)
    return answer


def literal(colors, queries):
    out = []
    for i, c in queries:
        ds = [abs(i - j) for j, x in enumerate(colors) if x == c]
        out.append(min(ds) if ds else -1)
    return out


def checked(colors, queries):
    got = shortest_distance_color(colors, queries)
    assert got == literal(colors, queries), (colors, queries, got)
    return got


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def main():
    print(f"example 1: {checked([1, 1, 2, 1, 3, 2, 2, 3, 3], [[1, 3], [2, 2], [6, 1]])}")
    print(f"example 2: {checked([1, 2], [[0, 3]])}")
    print(f"small 1: {checked([2], [[0, 1], [0, 2], [0, 3]])}")
    print(f"small 2: {checked([3, 3, 3, 1], [[0, 1], [3, 3], [1, 2]])}")
    print(f"small 3: {checked([1, 2, 2, 2, 2, 2, 3], [[3, 1], [3, 3], [4, 3], [2, 1]])}")
    seed = Seed(1182)
    checksum = 0
    for t in range(2000):
        n = 1 + seed.next() % 15
        palette = 1 + seed.next() % 3
        colors = [1 + seed.next() % palette for _ in range(n)]
        queries = [[seed.next() % n, 1 + seed.next() % 3] for _ in range(5)]
        for d in checked(colors, queries):
            checksum = (checksum * 31 + d + 2 + t) % 1000000007
    print(f"2000 random arrays: checksum {checksum}")
    colors = [3 if i % 9973 == 0 else 1 + seed.next() % 2 for i in range(50000)]
    queries = [[seed.next() % 50000, 1 + seed.next() % 3] for _ in range(50000)]
    print(f"50000 colours, 50000 queries: {sum(shortest_distance_color(colors, queries))}")


main()
