# LeetCode #1599: Maximum Profit of Operating a Centennial Wheel
# -- the bench in Python, mirroring wheel.kara: the wheel run rotation by
# rotation, on 300 days of 100000 arrivals, all drawn first.


def min_operations_max_profit(customers, boarding_cost, running_cost):
    waiting = profit = best = rotations = 0
    answer = -1
    n = len(customers)
    while rotations < n or waiting > 0:
        if rotations < n:
            waiting += customers[rotations]
        board = min(waiting, 4)
        waiting -= board
        profit += board * boarding_cost - running_cost
        rotations += 1
        if profit > best:
            best = profit
            answer = rotations
    return answer


def main():
    seed = 1599

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    days = []
    for _ in range(300):
        customers = [next_random() % 9 for _ in range(100000)]
        boarding = next_random() % 100 + 1
        running = next_random() % 100 + 1
        days.append((customers, boarding, running))
    check = 0
    for customers, boarding, running in days:
        answer = min_operations_max_profit(customers, boarding, running)
        check = (check * 31 + answer + 1) % 1000000007
    print(f"300 days of 100000 arrivals: checksum {check}")


main()
