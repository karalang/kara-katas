# LeetCode #1723: Find Minimum Time to Finish All Jobs -- the bench, the
# Python mirror of the ★ arm: backtracking, the longest job first, a
# branch cut once it cannot beat the best finish, and only the first idle
# worker tried.


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


def main():
    count = 100
    rounds = 5
    n = 12
    seed = [1723]
    problems = []
    for _ in range(count):
        jobs = [wide(seed) % 10000000 + 1 for _ in range(n)]
        k = next_random(seed) % 11 + 2
        problems.append((jobs, k))
    total = 0
    check = 0
    for r in range(rounds):
        for jobs, k in problems:
            answer = minimum_time_required(jobs, k)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} jobs, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
