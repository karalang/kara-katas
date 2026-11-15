# LeetCode #2188: Minimum Time to Finish the Race -- the benchmark's
# Python mirror of race.kara: the runs on one tire, then the laps bottom
# up.


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


seed = 2188


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def main():
    row = []
    for _ in range(100000):
        f = big_random() % 100 + 1
        r = next_random() % 4 + 2
        row.append([f, r])
    check = 0
    for _ in range(5000):
        start = big_random() % 99901
        change_time = big_random() % 100000 + 1
        num_laps = 1000
        t = minimum_finish_time([list(p) for p in row[start:start + 100]], change_time, num_laps)
        check = (check * 31 + t % 1000000007) % 1000000007
    print(f"5000 solves: checksum {check}")


main()
