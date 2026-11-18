# LeetCode #2286: Booking Concert Tickets in Groups -- the Python mirror
# of the ★ arm, `booking.kara`.


class BookMyShow:
    def __init__(self, n, m):
        size = 1
        while size < n:
            size *= 2
        self.seats = m
        self.size = size
        self.most = [0] * (2 * size)
        self.free = [0] * (2 * size)
        for r in range(n):
            self.most[size + r] = m
            self.free[size + r] = m
        for p in range(size - 1, 0, -1):
            self.most[p] = max(self.most[2 * p], self.most[2 * p + 1])
            self.free[p] = self.free[2 * p] + self.free[2 * p + 1]

    def set(self, row, left):
        p = self.size + row
        self.most[p] = left
        self.free[p] = left
        p //= 2
        while p >= 1:
            self.most[p] = max(self.most[2 * p], self.most[2 * p + 1])
            self.free[p] = self.free[2 * p] + self.free[2 * p + 1]
            p //= 2

    def leftmost(self, k):
        if self.most[1] < k:
            return None
        p = 1
        while p < self.size:
            p = 2 * p if self.most[2 * p] >= k else 2 * p + 1
        return p - self.size

    def free_through(self, row):
        total = 0
        lo = self.size
        hi = self.size + row + 1
        while lo < hi:
            if lo % 2 == 1:
                total += self.free[lo]
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                total += self.free[hi]
            lo //= 2
            hi //= 2
        return total

    def gather(self, k, max_row):
        row = self.leftmost(k)
        if row is not None and row <= max_row:
            left = self.free[self.size + row]
            self.set(row, left - k)
            return [row, self.seats - left]
        return []

    def scatter(self, k, max_row):
        if self.free_through(max_row) < k:
            return False
        need = k
        while need > 0:
            row = self.leftmost(1)
            left = self.free[self.size + row]
            take = min(left, need)
            self.set(row, left - take)
            need -= take
        return True


# ---- test harness ---------------------------------------------------------

seed = 2286


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def show_list(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show_bool(b):
    return "true" if b else "false"


def run(n, m, calls, high):
    show = BookMyShow(n, m)
    check = 0
    booked = 0
    for _ in range(calls):
        k = wide_random() % high + 1
        max_row = next_random() % n
        if next_random() % 2 == 0:
            got = show.gather(k, max_row)
            if len(got) == 2:
                booked += k
                mark = (got[0] * 1000003 + got[1]) % 1000000007 + 3
            else:
                mark = 0
        elif show.scatter(k, max_row):
            booked += k
            mark = 1
        else:
            mark = 2
        check = (check * 31 + mark) % 1000000007
    return check, booked


def main():
    show = BookMyShow(2, 5)
    a = show_list(show.gather(4, 0))
    b = show_list(show.gather(2, 0))
    c = show_bool(show.scatter(5, 1))
    d = show_bool(show.scatter(5, 1))
    print(f"{a} {b} {c} {d}")
    show = BookMyShow(3, 4)
    parts = [
        show_list(show.gather(4, 0)),
        show_list(show.gather(1, 0)),
        show_list(show.gather(3, 2)),
        show_bool(show.scatter(5, 2)),
        show_bool(show.scatter(1, 2)),
    ]
    print(" ".join(parts))
    check = 0
    booked = 0
    for _ in range(400):
        n = next_random() % 20 + 1
        m = next_random() % 20 + 1
        calls = next_random() % 60 + 1
        c, b = run(n, m, calls, 2 * m)
        check = (check * 31 + c) % 1000000007
        booked += b
    print(f"400 shows: checksum {check}, {booked} seats booked")
    c, b = run(2000, 1000000000, 5000, 2000000000)
    print(f"2000 rows of 10^9: checksum {c}, {b} seats booked")


main()
