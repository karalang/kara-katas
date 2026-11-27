# LeetCode #1845: Seat Reservation Manager -- the bench in Python: the ★ arm,
# every unreserved seat in a heapq heap, over 50 runs of 10^5 calls on
# 50000 to 99999 seats, each run's size and its place in one list of 10^6
# draws, built once, taken from the checksum so far. A draw reserves a seat
# two times in three, and otherwise gives back a held seat it picks; every
# seat reserved goes into the checksum.
import heapq


class SeatManager:
    def __init__(self, n):
        self.free = list(range(1, n + 1))
        heapq.heapify(self.free)

    def reserve(self):
        return heapq.heappop(self.free)

    def unreserve(self, seat_number):
        heapq.heappush(self.free, seat_number)


def main():
    seed = 1845
    draws = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        draws.append(seed // 65536)
    check = 0
    for _ in range(50):
        n = 50000 + check % 50000
        start = check % 500000
        seats = SeatManager(n)
        held = []
        for k in range(100000):
            d = draws[start + k]
            if not held or (d % 3 != 0 and len(held) < n):
                seat = seats.reserve()
                check = (check * 31 + seat) % 1000000007
                held.append(seat)
            else:
                i = d % len(held)
                held[i], held[-1] = held[-1], held[i]
                seats.unreserve(held.pop())
    print(f"50 runs: checksum {check}")


main()
