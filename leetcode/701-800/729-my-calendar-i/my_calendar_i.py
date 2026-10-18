# LeetCode #729: My Calendar I -- every booking checked in turn.
# Mirror of the Kara star arm and its harness.


class MyCalendar:
    def __init__(self):
        self.booked = []

    def book(self, start, end):
        for s, e in self.booked:
            if start < e and s < end:
                return False
        self.booked.append((start, end))
        return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def run(bookings):
    cal = MyCalendar()
    return [cal.book(s, e) for s, e in bookings]


def show(bookings):
    res = "[" + ", ".join("true" if r else "false" for r in run(bookings)) + "]"
    print(f"{bookings} -> {res}")


def count(what, bookings):
    print(f"{what} -> {sum(run(bookings))} accepted")


def main():
    show([(10, 20), (15, 25), (20, 30)])
    show([(10, 20), (5, 10), (20, 21), (9, 11), (0, 5)])
    show([(47, 50), (33, 41), (39, 45), (33, 42), (25, 32), (26, 35), (19, 25), (3, 8), (8, 13), (18, 27)])
    show([(0, 1000000000), (0, 1), (999999999, 1000000000)])
    show([(5, 6), (5, 6), (4, 5), (6, 7), (4, 7)])
    seed = [729]
    rnd = []
    for _ in range(1000):
        s = (next_random(seed) * 32768 + next_random(seed)) % 1000000000
        length = 1 + (next_random(seed) * 32768 + next_random(seed)) % 1000000
        rnd.append((s, min(s + length, 1000000000)))
    count("1000 random bookings up to 10^9", rnd)
    count("1000 bookings end to end, rising", [(i * 10, i * 10 + 10) for i in range(1000)])
    count("1000 bookings end to end, falling", [(10000 - i * 10 - 10, 10000 - i * 10) for i in range(1000)])
    count("1000 bookings around one point", [(500 - i // 2, 501 + i // 2) for i in range(1000)])
    total = 0
    accepted = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 20
        bookings = []
        for _ in range(n):
            s = next_random(seed) % 100
            e = s + 1 + next_random(seed) % 15
            bookings.append((s, e))
        for r in run(bookings):
            v = 1 if r else 0
            accepted += v
            total = (total * 131 + v + 1) % 1000000007
    print(f"300 random runs: {accepted} accepted, checksum {total}")


main()
