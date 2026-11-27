# LeetCode #1845: Seat Reservation Manager -- the ★ arm in Python, with
# heapq as the queue of unreserved seats
import heapq


class SeatManager:
    def __init__(self, n):
        self.free = list(range(1, n + 1))
        heapq.heapify(self.free)

    def reserve(self):
        return heapq.heappop(self.free)

    def unreserve(self, seat_number):
        heapq.heappush(self.free, seat_number)


seed = 1845


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(n, ops):
    seats = SeatManager(n)
    out = []
    for op in ops:
        if op == 0:
            out.append(seats.reserve())
        else:
            seats.unreserve(op)
    return out


def run_drawn(n, length):
    seats = SeatManager(n)
    held = []
    out = []
    for _ in range(length):
        if len(held) < n and (not held or next_random() % 5 < 3):
            seat = seats.reserve()
            held.append(seat)
            out.append(seat)
        else:
            at = next_random() % len(held)
            held[at], held[-1] = held[-1], held[at]
            seat = held.pop()
            seats.unreserve(seat)
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(run(5, [0, 0, 2, 0, 0, 0, 0, 5])))
    print(f"{show(run(1, [0, 1, 0, 1, 0]))} {show(run(4, [0, 0, 0, 0]))} {show(run(5, [0, 0, 0, 3, 1, 0, 0]))}")
    drawn = 0
    for x in run_drawn(100000, 100000):
        drawn = (drawn * 31 + x) % 1000000007
    full = 0
    for x in run(100000, [0] * 100000):
        full = (full * 31 + x) % 1000000007
    print(f"the most: {drawn} {full}")
    check = 0
    reserved = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        length = 1 + next_random() % 60
        for x in run_drawn(n, length):
            reserved += 1
            check = (check * 31 + x) % 1000000007
    print(f"300 random runs: {reserved} reservations, checksum {check}")


main()
