# LeetCode #731: My Calendar II -- mirror of the star arm.


class MyCalendarTwo:
    def __init__(self):
        self.booked = []
        self.doubled = []

    def book(self, start, end):
        for d in self.doubled:
            if start < d[1] and d[0] < end:
                return False
        for b in self.booked:
            if start < b[1] and b[0] < end:
                self.doubled.append((max(start, b[0]), min(end, b[1])))
        self.booked.append((start, end))
        return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(bookings):
    cal = MyCalendarTwo()
    return [cal.book(s, e) for s, e in bookings]


def fmt(bookings):
    return "[" + ", ".join(f"({s}, {e})" for s, e in bookings) + "]"


def show(bookings):
    out = "[" + ", ".join("true" if r else "false" for r in run(bookings)) + "]"
    print(f"{fmt(bookings)} -> {out}")


def count(what, bookings):
    print(f"{what} -> {sum(1 for r in run(bookings) if r)} accepted")


def main():
    global seed
    show([(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)])
    show([(0, 10), (0, 10), (0, 10), (10, 20), (10, 20), (5, 15)])
    show([(24, 40), (43, 50), (27, 43), (5, 21), (30, 40), (14, 29), (3, 19), (3, 14), (25, 39), (6, 19)])
    show([(0, 1000000000), (0, 1), (999999999, 1000000000), (0, 1000000000)])
    show([(5, 6), (5, 6), (5, 6), (4, 5), (6, 7), (4, 7), (4, 7)])
    seed = 731
    rnd = []
    for _ in range(1000):
        s = (next_random() * 32768 + next_random()) % 1000000000
        ln = 1 + (next_random() * 32768 + next_random()) % 1000000
        rnd.append((s, min(s + ln, 1000000000)))
    count("1000 random bookings up to 10^9", rnd)
    count("1000 bookings, each over the next two, rising", [(i * 10, i * 10 + 25) for i in range(1000)])
    count("1000 bookings, each over the next two, falling", [(10000 - i * 10, 10025 - i * 10) for i in range(1000)])
    count("1000 bookings around one point", [(500 - i // 2, 501 + i // 2) for i in range(1000)])
    total = 0
    accepted = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        bookings = []
        for _ in range(n):
            s = next_random() % 100
            e = s + 1 + next_random() % 15
            bookings.append((s, e))
        for r in run(bookings):
            v = 1 if r else 0
            accepted += v
            total = (total * 131 + v + 1) % 1000000007
    print(f"300 random runs: {accepted} accepted, checksum {total}")


main()
