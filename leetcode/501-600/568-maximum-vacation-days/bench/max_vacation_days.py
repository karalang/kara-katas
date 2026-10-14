# Benchmark for #568: Python mirror of the ★ arm (dynamic programming
# over the weeks); see max_vacation_days.kara.


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


# ---- benchmark --------------------------------------------------------------

seed = 568


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    rounds = 30
    densities = [1, 2, 5, 10, 25, 50, 100]
    cases = []
    for g in range(count):
        density = densities[g % 7]
        flights = []
        for i in range(100):
            row = [0] * 100
            for j in range(100):
                if i != j and step() % 100 < density:
                    row[j] = 1
            flights.append(row)
        days = []
        for _ in range(100):
            row = [0] * 100
            for w in range(100):
                row[w] = step() % 8
            days.append(row)
        cases.append((flights, days))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            flights, days = cases[(rnd * 7 + g) % count]
            got = max_vacation_days(flights, days)
            total += got
            checksum = (checksum * 31 + got + 1) % 1000000007
    print(f"{count} cases of 100 cities and 100 weeks, {rounds} rounds: {total} days, checksum {checksum}")


main()
