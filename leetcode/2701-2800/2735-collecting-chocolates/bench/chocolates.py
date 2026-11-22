# LeetCode #2735: Collecting Chocolates -- the bench (chocolates.kara in
# Python): each type's cheapest price within k turns, narrowed one turn at
# a time, and the least of k x plus their sum.


def min_cost(nums, x):
    n = len(nums)
    cheapest = list(nums)
    best = sum(nums)
    for k in range(1, n):
        for t in range(n):
            v = nums[(t - k + n) % n]
            if v < cheapest[t]:
                cheapest[t] = v
        best = min(best, k * x + sum(cheapest))
    return best


seed = 2735


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases, n, rounds = 100, 1000, 3
    problems = []
    for _ in range(cases):
        nums = [(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(n)]
        x = (next_random() * 32768 + next_random()) % 10000000 + 1
        problems.append((nums, x))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, x in problems:
            cost = min_cost(nums, x)
            total += cost
            check = (check * 31 + cost + r) % 1000000007
    print(f"{cases} cases of {n} chocolates, {rounds} rounds: costs sum to {total}, checksum {check}")


main()
