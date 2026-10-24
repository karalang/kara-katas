# Benchmark: LeetCode #973 K Closest Points to Origin -- the ★ arm, sort
# by squared distance, on 100 sets of 1000 random points. Mirrors
# k_closest.kara, .rs, .c and go-seq/.


def k_closest(points, k):
    s = sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])
    return s[:k]


seed = 973


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n):
    points = []
    for _ in range(n):
        x = next_random() % 20001 - 10000
        y = next_random() % 20001 - 10000
        points.append((x, y))
    ds = sorted(x * x + y * y for x, y in points)
    k = 1 + next_random() % n
    while k < n and ds[k - 1] == ds[k]:
        k += 1
    return points, k


def main():
    rounds = count = 100
    cases = [random_case(1000) for _ in range(count)]
    kept = check = 0
    for r in range(rounds):
        for i in range(count):
            points, k = cases[(r + i) % count]
            answer = k_closest(points, k)
            kept += len(answer)
            for x, y in answer:
                v = ((x + 10001) * 20003 + y + 10001) % 1000000007
                check = (check + v * v) % 1000000007
    print(f"{rounds} rounds over {count} sets of 1000 points: "
          f"{kept} points kept, checksum {check}")


main()
