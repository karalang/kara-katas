# LeetCode #732: My Calendar III -- starts and ends, merged.
# Benchmark mirror of the Kara star arm: keep the starts and the ends
# in two sorted lists, each put in its place by binary search, and
# sweep both together for the most bookings at once.


def place(v, x):
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        if v[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    v.insert(lo, x)


class MyCalendarThree:
    def __init__(self):
        self.starts = []
        self.ends = []

    def book(self, start, end):
        place(self.starts, start)
        place(self.ends, end)
        starts, ends = self.starts, self.ends
        n = len(starts)
        i = j = now = most = 0
        while i < n:
            if ends[j] <= starts[i]:
                now -= 1
                j += 1
            else:
                now += 1
                i += 1
                if now > most:
                    most = now
        return most


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [732]
    lists = []
    for _ in range(20):
        bookings = []
        for _ in range(1000):
            s = (next_random(seed) * 32768 + next_random(seed)) % 998999000
            length = 1 + (next_random(seed) * 32768 + next_random(seed)) % 1000000
            bookings.append((s, s + length))
        lists.append(bookings)
    total = 0
    for rnd in range(40):
        for d in range(20):
            cal = MyCalendarThree()
            for s, e in lists[d]:
                total += cal.book(s + rnd, e + rnd)
    print(f"40 rounds of 20 lists of 1000 bookings: answers sum {total}")


main()
