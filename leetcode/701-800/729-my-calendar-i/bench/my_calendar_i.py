# LeetCode #729: My Calendar I -- every booking checked in turn.
# Benchmark mirror of the Kara star arm: keep the accepted bookings in
# a list and accept a new one only if it overlaps none of them.


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


def main():
    seed = [729]
    lists = []
    for _ in range(20):
        bookings = []
        for _ in range(1000):
            s = (next_random(seed) * 32768 + next_random(seed)) % 998999000
            length = 1 + (next_random(seed) * 32768 + next_random(seed)) % 1000000
            bookings.append((s, s + length))
        lists.append(bookings)
    accepted = 0
    for rnd in range(80):
        for d in range(20):
            cal = MyCalendar()
            for s, e in lists[d]:
                if cal.book(s + rnd, e + rnd):
                    accepted += 1
    print(f"80 rounds of 20 lists of 1000 bookings: {accepted} accepted")


main()
