# LeetCode #1723: Find Minimum Time to Finish All Jobs -- the Python
# mirror of the ★ arm, jobs.kara: backtracking, the longest job first, a
# branch cut once it cannot beat the best finish, and only the first idle
# worker tried.
import sys

sys.setrecursionlimit(10000)


def place(jobs, i, loads, best):
    if i == len(jobs):
        best[0] = max(loads)
        return
    for w in range(len(loads)):
        if loads[w] + jobs[i] < best[0]:
            loads[w] += jobs[i]
            place(jobs, i + 1, loads, best)
            loads[w] -= jobs[i]
        if loads[w] == 0:
            break


def minimum_time_required(jobs, k):
    order = sorted(jobs, reverse=True)
    best = [sum(order) + 1]
    place(order, 0, [0] * k, best)
    return best[0]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide(seed):
    return next_random(seed) * 32768 + next_random(seed)


def batch(count, least, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = least + next_random(seed) % (most - least + 1)
        jobs = [wide(seed) % top + 1 for _ in range(n)]
        k = next_random(seed) % n + 1
        answer = minimum_time_required(jobs, k)
        total += answer
        check = (check * 31 + answer + n + k) % 1000000007
    print(f"{count} problems of {least} to {most} jobs up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(minimum_time_required([3, 2, 3], 3))
    print(minimum_time_required([1, 2, 4, 7, 8], 2))
    print(minimum_time_required([5], 1))
    print(minimum_time_required([10000000] * 12, 12))
    print(minimum_time_required([10000000] * 12, 1))
    seed = [1723]
    batch(3000, 1, 6, 10, seed)
    batch(300, 1, 10, 10000000, seed)
    batch(20, 12, 12, 10000000, seed)


main()
