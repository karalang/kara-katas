# LeetCode #1235 bench: the ★ arm in Python, over the same 20 sets of 50000
# jobs and 10 passes as the Kāra bench.

from bisect import bisect_right


def job_scheduling(start_time, end_time, profit):
    n = len(start_time)
    order = sorted(range(n), key=lambda i: end_time[i])
    ends = [end_time[i] for i in order]
    best = [0] * (n + 1)
    for k in range(n):
        job = order[k]
        before = bisect_right(ends, start_time[job])
        best[k + 1] = max(best[k], best[before] + profit[job])
    return best[n]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1235]
    sets = []
    for t in range(20):
        long = 1000000 * (t % 4 + 1)
        start, end, profit = [], [], []
        for _ in range(50000):
            a = next_random(seed) * 32768
            s = (a + next_random(seed)) % 999000000 + 1
            start.append(s)
            b = next_random(seed) * 32768
            end.append(s + (b + next_random(seed)) % long + 1)
            profit.append(next_random(seed) % 10000 + 1)
        sets.append((start, end, profit))
    check = 0
    for _ in range(10):
        for start, end, profit in sets:
            check = (check * 131 + job_scheduling(start, end, profit)) % 1000000007
    print(f"20 sets of 50000 jobs, 10 passes: checksum {check}")


main()
