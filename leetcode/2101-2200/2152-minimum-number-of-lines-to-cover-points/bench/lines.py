# LeetCode #2152: Minimum Number of Lines to Cover Points -- the
# benchmark's Python mirror of lines.kara.


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


def free_place(points):
    while True:
        x = next_random() % 7 - 3
        y = next_random() % 7 - 3
        if [x, y] not in points:
            return [x, y]


def main():
    sets = []
    for _ in range(4):
        points = []
        while len(points) < 10:
            points.append(free_place(points))
        sets.append(points)
    total = 0
    check = 0
    for rnd in range(2500):
        for s in range(4):
            at = next_random() % 10
            sets[s][at] = free_place(sets[s])
            lines = minimum_lines(sets[s])
            total += lines
            check = (check * 31 + lines + rnd) % 1000000007
    print(f"10000 solves: {total} lines in all, checksum {check}")


main()
