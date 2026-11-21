# LeetCode #2463: Minimum Total Distance Traveled -- the Python mirror of
# distance.kara: a table over the sorted robots and factories, each
# factory either skipped or given the next run of robots up to its limit.

NONE = 9000000000000000000


def minimum_total_distance(robot, factory):
    robots = sorted(robot)
    factories = sorted(factory)
    n, m = len(robots), len(factories)
    best = [[NONE] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        best[n][j] = 0
    for j in range(m - 1, -1, -1):
        at, limit = factories[j]
        for i in range(n - 1, -1, -1):
            least = best[i][j + 1]
            run = 0
            for t in range(1, min(limit, n - i) + 1):
                run += abs(robots[i + t - 1] - at)
                if best[i + t][j + 1] < NONE:
                    least = min(least, run + best[i + t][j + 1])
            best[i][j] = least
    return best[0][0]


# ---- test harness ---------------------------------------------------------

seed = 2463


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_case(n, m, top, cap):
    taken = set()
    robot = []
    while len(robot) < n:
        p = wide_random() % (2 * top + 1) - top
        if p not in taken:
            taken.add(p)
            robot.append(p)
    places = set()
    factory = []
    while len(factory) < m:
        p = wide_random() % (2 * top + 1) - top
        if p not in places:
            places.add(p)
            factory.append([p, next_random() % (cap + 1)])
    room = sum(f[1] for f in factory)
    j = 0
    while room < n:
        factory[j % m][1] += 1
        room += 1
        j += 1
    return robot, factory


def show(values):
    return "[" + ", ".join(show(v) if isinstance(v, list) else str(v) for v in values) + "]"


def main():
    cases = [
        ([0, 4, 6], [[2, 2], [6, 2]]),
        ([1, -1], [[-2, 1], [2, 1]]),
        ([5], [[5, 1]]),
        ([0, 1], [[0, 0], [10, 2]]),
        ([1, 2, 3], [[2, 1], [100, 2]]),
        ([-1000000000, 1000000000], [[1000000000, 1], [-1000000000, 1]]),
    ]
    for robot, factory in cases:
        print(f"{show(robot)} {show(factory)} -> {minimum_total_distance(robot, factory)}")
    r1, f1 = random_case(100, 100, 1000000000, 3)
    print(f"100 robots, 100 factories over 2 10^9: {minimum_total_distance(r1, f1)}")
    r2, f2 = random_case(100, 3, 1000000000, 0)
    print(f"100 robots, 3 factories: {minimum_total_distance(r2, f2)}")
    r3, f3 = random_case(100, 100, 100, 2)
    print(f"100 robots, 100 factories over 201 places: {minimum_total_distance(r3, f3)}")
    check = 0
    for _ in range(1000):
        n = 1 + next_random() % 6
        m = 1 + next_random() % 4
        robot, factory = random_case(n, m, 10, 3)
        check = (check * 31 + minimum_total_distance(robot, factory)) % 1000000007
    print(f"1000 random: checksum {check}")


if __name__ == "__main__":
    main()
