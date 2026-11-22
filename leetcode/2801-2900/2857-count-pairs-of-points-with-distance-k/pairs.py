# LeetCode #2857: Count Pairs of Points With Distance k -- the ★ arm's
# mirror: each point looks up its k + 1 candidate partners among the
# points before it, counted in a dict, and is then counted itself.


def count_pairs(coordinates, k):
    seen = {}
    pairs = 0
    for x, y in coordinates:
        for a in range(k + 1):
            pairs += seen.get((x ^ a, y ^ (k - a)), 0)
        seen[(x, y)] = seen.get((x, y), 0) + 1
    return pairs


seed = 2857


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def points(n, top):
    out = []
    for _ in range(n):
        x = wide() % top
        y = wide() % top
        out.append([x, y])
    return out


def main():
    first = [[1, 2], [4, 2], [1, 3], [5, 2]]
    second = [[1, 3] for _ in range(5)]
    print(f"{count_pairs(first, 5)} {count_pairs(second, 0)}")
    same = [[1000000, 1000000] for _ in range(50000)]
    line = [[i, 0] for i in range(50000)]
    print(f"{count_pairs(same, 0)} {count_pairs(line, 1)}")
    total = check = 0
    for c in range(3010):
        small = c < 3000
        n = next_random() % 8 + 2 if small else wide() % 40001 + 10000
        top = 8 if small else (64 if c % 2 == 0 else 1000001)
        k = next_random() % 11 if small else next_random() % 101
        pairs = count_pairs(points(n, top), k)
        total += pairs
        check = (check * 31 + pairs) % 1000000007
        if c == 2999:
            print(f"3000 short cases: {total} pairs, checksum {check}")
            total = check = 0
    print(f"10 long cases: {total} pairs, checksum {check}")


main()
