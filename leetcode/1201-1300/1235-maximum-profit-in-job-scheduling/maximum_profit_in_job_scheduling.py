# LeetCode #1235: Maximum Profit in Job Scheduling -- Python mirror of the ★
# arm: dynamic programming over the jobs sorted by end time, the jobs that
# end by each start counted by a binary search on the sorted ends.

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


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def jobs(n, span, long, seed):
    start, end, profit = [], [], []
    for _ in range(n):
        s = next_random(seed) * 32768 % span + next_random(seed) % span
        s = s % span + 1
        start.append(s)
        end.append(s + next_random(seed) * 32768 % long + 1)
        profit.append(next_random(seed) % 10000 + 1)
    return start, end, profit


def main():
    print(job_scheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]))
    print(job_scheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]))
    print(job_scheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]))
    print(job_scheduling([7], [9], [4]))
    seed = [1235]
    check = 0
    for _ in range(1000):
        n = next_random(seed) % 30 + 1
        start, end, profit = jobs(n, 40, next_random(seed) % 10 + 1, seed)
        check = (check * 131 + job_scheduling(start, end, profit)) % 1000000007
    print(f"1000 random sets: checksum {check}")
    start, end, profit = jobs(50000, 999000000, 1000000, seed)
    every = [i % 10000 + 1 for i in range(50000)]
    chain = [i * 20000 + 1 for i in range(50000)]
    after = [s + 20000 for s in chain]
    a = job_scheduling(start, end, profit)
    b = job_scheduling([1] * 50000, [1000000000] * 50000, every)
    c = job_scheduling(chain, after, every)
    print(f"5 * 10^4 jobs: {a}, {b}, {c}")


main()
