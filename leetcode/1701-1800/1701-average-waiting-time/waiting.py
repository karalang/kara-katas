# LeetCode #1701: Average Waiting Time -- mirrors waiting.kara, the ★ arm:
# the chef's finishing time carried from customer to customer.

import math


def average_waiting_time(customers):
    finish = 0
    waited = 0
    for arrival, time in customers:
        finish = max(finish, arrival) + time
        waited += finish - arrival
    return waited / len(customers)


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, gap, top, seed):
    total = 0.0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        customers = []
        arrival = 0
        for _ in range(n):
            arrival += seed.next() % (gap + 1)
            customers.append([arrival + 1, seed.next() % top + 1])
        answer = average_waiting_time(customers)
        total += answer
        # Kāra's round() takes a half away from zero; Python's round() to even
        check = (check * 31 + math.floor(answer * 100000.0 + 0.5)) % 1000000007
    print(f"{count} lists of up to {most} customers: answers sum to {total:.5f}, checksum {check}")


def main():
    print(f"{average_waiting_time([[1, 2], [2, 5], [4, 3]]):.5f}")
    print(f"{average_waiting_time([[5, 2], [5, 4], [10, 3], [20, 1]]):.5f}")
    print(f"{average_waiting_time([[7, 4]]):.5f}")
    print(f"{average_waiting_time([[1, 1], [1, 1], [1, 1]]):.5f}")
    seed = Seed(1701)
    batch(3000, 12, 5, 5, seed)
    batch(300, 1000, 100, 100, seed)
    batch(10, 100000, 10000, 10000, seed)


main()
