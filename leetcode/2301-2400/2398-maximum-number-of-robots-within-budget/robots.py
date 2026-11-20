# LeetCode #2398: Maximum Number of Robots Within Budget -- a Python
# mirror of the ★ arm: a sliding window, its largest charge time kept by
# a monotonic deque. Prints the same output as robots.kara.

from collections import deque

seed = 0


def maximum_robots(charge_times, running_costs, budget):
    best = 0
    left = 0
    total = 0
    largest = deque()
    for right in range(len(charge_times)):
        total += running_costs[right]
        while largest and charge_times[largest[-1]] <= charge_times[right]:
            largest.pop()
        largest.append(right)
        while left <= right and charge_times[largest[0]] + (right - left + 1) * total > budget:
            if largest[0] == left:
                largest.popleft()
            total -= running_costs[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def main():
    global seed
    print(maximum_robots([3, 6, 1, 3, 4], [2, 1, 3, 4, 5], 25))
    print(maximum_robots([11, 12, 19], [10, 8, 7], 19))
    print(f"{maximum_robots([5], [4], 9)} {maximum_robots([5], [4], 8)} {maximum_robots([1, 1, 1], [1, 1, 1], 10)}")
    seed = 2398
    n = 50000
    charge = [1 + wide() % 100000 for _ in range(n)]
    running = [1 + wide() % 100000 for _ in range(n)]
    answers = []
    budget = 100000
    while budget <= 10**15:
        answers.append(maximum_robots(charge, running, budget))
        budget *= 10
    print(f"5 * 10^4 robots: [{', '.join(map(str, answers))}]")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 100
        charge = [1 + next_random() % top for _ in range(n)]
        running = [1 + next_random() % top for _ in range(n)]
        budget = 1 + wide() % (top * 40 * (1 + n))
        k = maximum_robots(charge, running, budget)
        check = (check * 31 + k) % 1000000007
        total += k
    print(f"3000 fleets: checksum {check}, {total} robots in all")


if __name__ == "__main__":
    main()
