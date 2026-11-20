# LeetCode #2398: Maximum Number of Robots Within Budget -- the bench, the
# ★ arm in Python: a sliding window, its largest charge time kept by a
# monotonic deque.

from collections import deque

seed = 2398


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
    fleets = []
    for _ in range(20):
        charge = [1 + wide() % 100000 for _ in range(50000)]
        running = [1 + wide() % 100000 for _ in range(50000)]
        fleets.append((charge, running))
    check = 0
    for p in range(2):
        for charge, running in fleets:
            budget = 100000
            while budget <= 10**15:
                check = (check * 31 + maximum_robots(charge, running, budget) + p) % 1000000007
                budget *= 10
    print(f"2 passes over 20 fleets of 5 * 10^4 robots, 11 budgets: checksum {check}")


if __name__ == "__main__":
    main()
