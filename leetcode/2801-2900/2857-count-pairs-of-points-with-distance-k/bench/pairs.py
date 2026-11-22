# LeetCode #2857: Count Pairs of Points With Distance k -- the bench:
# the ★ arm over 10 cases of 50000 points, LeetCode's most, every
# other one in a 256 x 256 square and the rest up to 10^6, with k up
# to 100, all drawn first, then each answered 3 times.


def count_pairs(coordinates, k):
    seen = {}
    pairs = 0
    for x, y in coordinates:
        for a in range(k + 1):
            pairs += seen.get((x ^ a, y ^ (k - a)), 0)
        seen[(x, y)] = seen.get((x, y), 0) + 1
    return pairs


def main():
    count, rounds, n = 10, 3, 50000
    seed = 2857

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    cases = []
    for c in range(count):
        top = 256 if c % 2 == 0 else 1000001
        k = nr() % 101
        points = []
        for _ in range(n):
            x = wide() % top
            y = wide() % top
            points.append([x, y])
        cases.append((points, k))
    total = check = 0
    for r in range(rounds):
        for points, k in cases:
            pairs = count_pairs(points, k)
            total += pairs
            check = (check * 31 + pairs + r) % 1000000007
    print(f"{count} cases of {n} points, {rounds} rounds: {total} pairs, checksum {check}")


main()
