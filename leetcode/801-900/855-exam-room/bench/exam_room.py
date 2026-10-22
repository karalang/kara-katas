# Benchmark for #855: Exam Room -- the sorted-vector arm, mirroring
# exam_room.kara.
import bisect


class ExamRoom:
    def __init__(self, n):
        self.n = n
        self.taken = []

    def seat(self):
        taken = self.taken
        if not taken:
            taken.append(0)
            return 0
        best = taken[0]
        best_seat = 0
        for i in range(len(taken) - 1):
            half = (taken[i + 1] - taken[i]) // 2
            if half > best:
                best = half
                best_seat = taken[i] + half
        last = taken[-1]
        if self.n - 1 - last > best:
            best_seat = self.n - 1
        lo, hi = 0, len(taken)
        while lo < hi:
            mid = (lo + hi) // 2
            if taken[mid] < best_seat:
                lo = mid + 1
            else:
                hi = mid
        taken.insert(lo, best_seat)
        return best_seat

    def leave(self, p):
        del self.taken[bisect.bisect_left(self.taken, p)]


seed = 855


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, calls, n = 300, 4000, 1000000000
    total = 0
    checksum = 0
    for _ in range(rounds):
        room = ExamRoom(n)
        seated = []
        for _ in range(calls):
            if not seated or next_random() % 3 != 0:
                p = room.seat()
                seated.append(p)
                total += p
                checksum = (checksum * 31 + p % 1000003) % 1000000007
            else:
                i = next_random() % len(seated)
                seated[i], seated[-1] = seated[-1], seated[i]
                p = seated.pop()
                room.leave(p)
    print(f"{rounds} rooms of 4000 calls: seats sum to {total}, checksum {checksum}")


main()
