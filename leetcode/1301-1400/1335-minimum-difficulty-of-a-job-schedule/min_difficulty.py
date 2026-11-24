# LeetCode #1335: Minimum Difficulty of a Job Schedule -- Python mirror of
# the ★ arm: the least difficulty of the first i jobs in so many days, one
# day at a time.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    ex = [min_difficulty([6, 5, 4, 3, 2, 1], 2), min_difficulty([9, 9, 9], 4), min_difficulty([1, 1, 1], 3)]
    print(f"{ex[0]} {ex[1]} {ex[2]} {min_difficulty([7], 1)} {min_difficulty([0, 0], 1)}")
    seed = 1335
    jobs = []
    rising = []
    for i in range(300):
        jobs.append(next_random() % 1001)
        rising.append(i * 3)
    print(f"300 jobs: {min_difficulty(jobs, 10)} {min_difficulty(jobs, 1)}, rising {min_difficulty(rising, 10)}")
    check = 0
    impossible = 0
    for t in range(300):
        n = 1 + next_random() % 300 if t % 25 == 0 else 1 + next_random() % 15
        top = 6 if t % 2 == 0 else 1001
        jd = [next_random() % top for _ in range(n)]
        d = 1 + next_random() % 10
        answer = min_difficulty(jd, d)
        if answer < 0:
            impossible += 1
        check = (check * 131 + answer + 7) % 1000000007
    print(f"300 random schedules: {impossible} impossible, checksum {check}")


main()
