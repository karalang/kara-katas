# LeetCode #1109: Corporate Flight Bookings -- the bench in Python: the ★
# arm (a difference array and a running total) over 16 problems of
# 2 * 10^4 flights and 2 * 10^4 bookings, each round changing one booking
# in every problem and solving it again.


def corp_flight_bookings(bookings, n):
    change = [0] * (n + 1)
    for b in bookings:
        change[b[0] - 1] += b[2]
        change[b[1]] -= b[2]
    seats = []
    running = 0
    for i in range(n):
        running += change[i]
        seats.append(running)
    return seats


seed = 1109


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def booking(n):
    a = next_random() % n + 1
    b = next_random() % n + 1
    return [min(a, b), max(a, b), next_random() % 10000 + 1]


def main():
    n = 20000
    problems = [[booking(n) for _ in range(20000)] for _ in range(16)]
    busiest = 0
    check = 0
    for rnd in range(200):
        for j in range(len(problems)):
            at = (rnd * 7919 + j * 104729) % 20000
            problems[j][at] = booking(n)
            seats = corp_flight_bookings(problems[j], n)
            busiest += max(seats)
            check = (check * 31 + seats[(rnd * 31 + j) % n]) % 1000000007
    print(f"200 rounds over 16 problems of 20000 flights: busiest total {busiest}, checksum {check}")


main()
