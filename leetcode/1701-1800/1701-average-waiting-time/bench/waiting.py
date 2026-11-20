# LeetCode #1701: Average Waiting Time -- the bench's Python mirror: the ★
# arm on 50 random lists of 100000 customers, arrivals and times up to
# 10^4, all drawn first, each answered 60 times.

import math


def average_waiting_time(customers):
    finish = 0
    waited = 0
    for arrival, time in customers:
        finish = max(finish, arrival) + time
        waited += finish - arrival
    return waited / len(customers)


seed = 1701


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 50, 60, 100000
    lists = []
    for _ in range(count):
        customers = []
        arrival = 0
        for _ in range(n):
            if next_random() % 10 == 0 and arrival < 9999:
                arrival += 1
            customers.append([arrival + 1, next_random() % 10000 + 1])
        lists.append(customers)
    total = 0.0
    check = 0
    for r in range(rounds):
        for customers in lists:
            answer = average_waiting_time(customers)
            total += answer
            # Kāra's round() takes a half away from zero; Python's round() to even
            check = (check * 31 + math.floor(answer * 100000.0 + 0.5) + r) % 1000000007
    print(f"{count} lists of {n} customers, {rounds} rounds: answers sum to {total:.5f}, checksum {check}")


main()
