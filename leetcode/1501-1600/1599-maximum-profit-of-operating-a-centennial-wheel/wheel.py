# LeetCode #1599: Maximum Profit of Operating a Centennial Wheel
# -- mirrors wheel.kara: the wheel run rotation by rotation.


def min_operations_max_profit(customers, boarding_cost, running_cost):
    waiting = profit = best = rotations = 0
    answer = -1
    while rotations < len(customers) or waiting > 0:
        if rotations < len(customers):
            waiting += customers[rotations]
        board = min(waiting, 4)
        waiting -= board
        profit += board * boarding_cost - running_cost
        rotations += 1
        if profit > best:
            best = profit
            answer = rotations
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def batch(count, most, seed):
    check = 0
    never = 0
    for _ in range(count):
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        customers = [next_random(seed) % 51 for _ in range(n)]
        boarding = next_random(seed) % 100 + 1
        running = next_random(seed) % 100 + 1
        answer = min_operations_max_profit(customers, boarding, running)
        if answer == -1:
            never += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} days of up to {most} arrivals: {never} never in profit, checksum {check}")


def main():
    examples = [
        ([8, 3], 5, 6),
        ([10, 9, 6], 6, 4),
        ([3, 4, 0, 5, 1], 1, 92),
        ([0, 0, 0], 5, 1),
        ([4], 1, 4),
        ([50, 50, 50], 100, 1),
        ([0, 0, 13], 10, 39),
    ]
    for customers, boarding, running in examples:
        shown = "[" + ", ".join(map(str, customers)) + "]"
        print(f"{shown}, {boarding}, {running} -> {min_operations_max_profit(customers, boarding, running)}")
    seed = [1599]
    batch(3000, 6, seed)
    batch(300, 100, seed)
    batch(3, 100000, seed)


main()
