# LeetCode #1136: Parallel Courses -- the bench, the ★ arm's algorithm:
# Kahn's algorithm a semester at a time.


def minimum_semesters(n, relations):
    after = [[] for _ in range(n + 1)]
    need = [0] * (n + 1)
    for r in relations:
        after[r[0]].append(r[1])
        need[r[1]] += 1
    now = [c for c in range(1, n + 1) if need[c] == 0]
    semesters = 0
    taken = 0
    while now:
        semesters += 1
        taken += len(now)
        upcoming = []
        for c in now:
            for d in after[c]:
                need[d] -= 1
                if need[d] == 0:
                    upcoming.append(d)
        now = upcoming
    return semesters if taken == n else -1


seed = 1136


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 5000
    plans = []
    for _ in range(8):
        plans.append([[next_random() % (c - 1) + 1, c] for c in range(2, n + 1)])
    total = 0
    check = 0
    for rnd in range(300):
        for j in range(8):
            at = (rnd * 7919 + j * 104729) % (n - 1)
            c = plans[j][at][1]
            plans[j][at][0] = next_random() % (c - 1) + 1
            r = minimum_semesters(n, plans[j])
            total += r
            check = (check * 31 + r + 1) % 1000000007
    print(f"300 rounds over 8 plans of 5000 courses and 4999 relations: semesters total {total}, checksum {check}")


main()
