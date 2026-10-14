# LeetCode #568: Maximum Vacation Days -- Python mirror of the ★ arm
# (dynamic programming over the weeks); see max_vacation_days.kara.


def max_vacation_days(flights, days):
    n = len(flights)
    k = len(days[0])
    best = [-1] * n
    best[0] = 0
    for w in range(k):
        nxt = [-1] * n
        for j in range(n):
            for i in range(n):
                if best[i] >= 0 and (i == j or flights[i][j] == 1):
                    nxt[j] = max(nxt[j], best[i] + days[j][w])
        best = nxt
    return max(best)


# ---- test harness ---------------------------------------------------------

seed = 568


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(label, flights, days):
    print(f"{label}: {max_vacation_days(flights, days)}")


def random_case(n, k, density, most):
    flights = []
    for i in range(n):
        row = [0] * n
        for j in range(n):
            if i != j and step() % 100 < density:
                row[j] = 1
        flights.append(row)
    days = []
    for _ in range(n):
        row = [0] * k
        for w in range(k):
            row[w] = step() % (most + 1)
        days.append(row)
    return flights, days


def main():
    show("example 1", [[0, 1, 1], [1, 0, 1], [1, 1, 0]], [[1, 3, 1], [6, 0, 3], [3, 3, 3]])
    show("example 2", [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [7, 7, 7], [7, 7, 7]])
    show("example 3", [[0, 1, 1], [1, 0, 1], [1, 1, 0]], [[7, 0, 0], [0, 7, 0], [0, 0, 7]])
    show("one city", [[0]], [[5]])
    show("chain", [[0, 1, 0], [0, 0, 1], [0, 0, 0]], [[7, 0, 0], [0, 0, 0], [0, 7, 7]])
    show("detour", [[0, 1, 1], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [7, 0, 0], [6, 6, 6]])
    show("back home", [[0, 1], [1, 0]], [[0, 7, 0, 7], [7, 0, 7, 0]])
    show("no days", [[0, 1], [1, 0]], [[0, 0], [0, 0]])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step() % 6
        k = 1 + step() % 6
        density = step() % 101
        flights, days = random_case(n, k, density, 7)
        got = max_vacation_days(flights, days)
        total += got
        checksum = (checksum * 31 + got + 1) % 1000000007
    print(f"300 random cases: {total} days, checksum {checksum}")
    every, days = random_case(100, 100, 100, 7)
    print(f"100 cities, 100 weeks, every flight: {max_vacation_days(every, days)}")
    some, days = random_case(100, 100, 2, 7)
    print(f"100 cities, 100 weeks, one flight in fifty: {max_vacation_days(some, days)}")
    ring = []
    for i in range(100):
        row = [0] * 100
        row[(i + 1) % 100] = 1
        ring.append(row)
    _, days = random_case(100, 100, 0, 7)
    print(f"100 cities, 100 weeks, a ring: {max_vacation_days(ring, days)}")


main()
