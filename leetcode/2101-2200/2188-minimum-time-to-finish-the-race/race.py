# LeetCode #2188: Minimum Time to Finish the Race -- the Python mirror of
# race.kara: the least time for each number of laps on one tire, then
# the laps laid out as runs between changes.


def minimum_finish_time(tires, change_time, num_laps):
    run = [0]
    for f, r in tires:
        lap = f
        total = 0
        k = 1
        while k <= num_laps and lap <= change_time + f:
            total += lap
            if k == len(run):
                run.append(total)
            elif total < run[k]:
                run[k] = total
            lap *= r
            k += 1
    best = [0] * (num_laps + 1)
    for n in range(1, num_laps + 1):
        least = run[1] * n + change_time * (n - 1)
        k = 1
        while k < len(run) and k <= n:
            pit = 0 if k == n else change_time
            least = min(least, best[n - k] + pit + run[k])
            k += 1
        best[n] = least
    return best[num_laps]


# ---- test harness ---------------------------------------------------------

seed = 2188


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def show(tires, change_time, num_laps):
    shown = ", ".join(f"[{f}, {r}]" for f, r in tires)
    print(f"[{shown}], {change_time}, {num_laps} -> {minimum_finish_time(tires, change_time, num_laps)}")


def main():
    show([[2, 3], [3, 4]], 5, 4)
    show([[1, 10], [2, 2], [3, 4]], 6, 5)
    show([[7, 2]], 3, 1)
    show([[1, 2]], 100000, 10)
    show([[5, 100000], [6, 2]], 1, 6)
    show([[100000, 100000]], 100000, 1000)
    total = 0
    check = 0
    for rnd in range(2000):
        big = rnd % 2 == 1
        n = next_random() % 10 + 1
        tires = []
        for _ in range(n):
            f = big_random() % 100000 + 1 if big else next_random() % 10 + 1
            r = big_random() % 99999 + 2 if big else next_random() % 4 + 2
            tires.append([f, r])
        change_time = big_random() % 100000 + 1 if big else next_random() % 20 + 1
        num_laps = next_random() % 1000 + 1 if big else next_random() % 20 + 1
        best = minimum_finish_time(tires, change_time, num_laps)
        total = (total + best) % 1000000007
        check = (check * 31 + best % 1000000007 + n) % 1000000007
    print(f"2000 races: {total} in all, checksum {check}")
    alike = []
    mixed = []
    for _ in range(100000):
        alike.append([1, 2])
        f = big_random() % 100000 + 1
        r = big_random() % 99999 + 2
        mixed.append([f, r])
    print(f"10^5 tires: {minimum_finish_time(alike, 1, 1000)} {minimum_finish_time(mixed, 100000, 1000)} {minimum_finish_time(mixed, 1, 1000)}")


main()
