# LeetCode #1335 bench, Python mirror of the Kāra bench: the ★ arm on 20
# schedules of 300 jobs built once, then 30 passes, each setting one job
# of every schedule and the number of days from the checksum so far,
# answering every schedule.


def min_difficulty(job_difficulty, d):
    n = len(job_difficulty)
    if n < d:
        return -1
    far = 1 << 62
    best = [far] * (n + 1)
    best[0] = 0
    for day in range(1, d + 1):
        nxt = [far] * (n + 1)
        for i in range(day, n + 1):
            hardest = 0
            m = far
            for j in range(i - 1, day - 2, -1):
                if job_difficulty[j] > hardest:
                    hardest = job_difficulty[j]
                v = best[j] + hardest
                if v < m:
                    m = v
            nxt[i] = m
        best = nxt
    return best[n]


seed = 1335


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 300
    schedules = [[next_random() % 1001 for _ in range(n)] for _ in range(20)]
    check = 0
    for p in range(30):
        d = 6 + check % 5
        for t in range(20):
            at = check % n
            schedules[t][at] = check // 3 % 1001
            answer = min_difficulty(schedules[t], d)
            check = (check * 31 + answer + p) % 1000000007
    print(f"30 passes over 20 schedules of 300 jobs: checksum {check}")


main()
