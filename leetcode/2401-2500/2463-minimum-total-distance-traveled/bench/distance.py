# LeetCode #2463: Minimum Total Distance Traveled -- the bench, the ★ arm
# in Python: a table over the sorted robots and factories, each factory
# either skipped or given the next run of robots up to its limit.

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


def main():
    # 40 cases of 100 robots and 100 factories over 2 10^9 places, limits
    # up to 2, built once; then 72 passes, each raising one limit of every
    # case, chosen by the checksum so far, then answering every case and
    # folding the answer plus the pass into the checksum
    cases = [random_case(100, 100, 1000000000, 2) for _ in range(40)]
    check = 0
    for p in range(72):
        for c, (robot, factory) in enumerate(cases):
            factory[(check + c) % 100][1] += 1
            check = (check * 31 + minimum_total_distance(robot, factory) % 1000000007 + p) % 1000000007
    print(f"72 passes over 40 cases of 100 robots: checksum {check}")


main()
