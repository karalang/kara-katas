# LeetCode #1109: Corporate Flight Bookings -- the Python mirror of the ★
# arm: a difference array and a running total over the flights.


def corp_flight_bookings(bookings, n):
    change = [0] * (n + 1)
    for first, last, seats in bookings:
        change[first - 1] += seats
        change[last] -= seats
    out = []
    running = 0
    for i in range(n):
        running += change[i]
        out.append(running)
    return out


seed = 1109


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bookings(n, m, most):
    bookings = []
    for _ in range(m):
        a = next_random() % n + 1
        b = next_random() % n + 1
        seats = next_random() % most + 1
        bookings.append([min(a, b), max(a, b), seats])
    return bookings


def fold(check, answer):
    for x in answer:
        check = (check * 31 + x) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        ([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5),
        ([[1, 2, 10], [2, 2, 15]], 2),
        ([[1, 1, 7]], 1),
        ([[1, 4, 3]], 4),
        ([[4, 4, 9], [1, 1, 2]], 4),
        ([[1, 3, 1], [1, 3, 1], [1, 3, 1]], 3),
        ([[2, 3, 10000], [1, 4, 10000]], 5),
        ([[3, 5, 6], [1, 2, 4], [2, 4, 8], [5, 5, 1]], 6),
    ]
    for bookings, n in cases:
        print(show(corp_flight_bookings(bookings, n)))
    seats = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        m = next_random() % 30 + 1
        answer = corp_flight_bookings(random_bookings(n, m, 100), n)
        seats += sum(answer)
        check = fold(check, answer)
    print(f"2000 random problems: {seats} seats, checksum {check}")
    answer = corp_flight_bookings(random_bookings(20000, 20000, 10000), 20000)
    print(f"20000 flights, 20000 bookings: busiest {max(answer)}, checksum {fold(0, answer)}")
    whole = [[1, 20000, i % 10000 + 1] for i in range(20000)]
    answer = corp_flight_bookings(whole, 20000)
    print(f"20000 bookings of every flight: {answer[0]} {answer[19999]}")


main()
