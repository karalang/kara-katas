# LeetCode #855: Exam Room -- Python mirror of the ★ arm (the taken seats
# kept sorted, scanned for the widest gap).
import bisect


class ExamRoom:
    def __init__(self, n):
        self.n = n
        self.taken = []

    def seat(self):
        best = 0
        best_seat = 0
        prev = -1
        for p in self.taken:
            if prev == -1:
                best = p
                best_seat = 0
            elif (p - prev) // 2 > best:
                best = (p - prev) // 2
                best_seat = prev + (p - prev) // 2
            prev = p
        if prev == -1:
            best_seat = 0
        elif self.n - 1 - prev > best:
            best_seat = self.n - 1
        bisect.insort(self.taken, best_seat)
        return best_seat

    def leave(self, p):
        self.taken.pop(bisect.bisect_left(self.taken, p))


def show(n, calls):
    room = ExamRoom(n)
    said = []
    got = []
    for c in calls:
        if c == -1:
            said.append("seat")
            got.append(str(room.seat()))
        else:
            said.append(f"leave {c}")
            room.leave(c)
    print(f"ExamRoom({n}): {', '.join(said)} -> {' '.join(got)}")


seed = 855


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_room(n, count):
    room = ExamRoom(n)
    seated = []
    total = 0
    check = 0
    for _ in range(count):
        full = len(seated) == n
        if not full and (not seated or next_random() % 3 != 0):
            p = room.seat()
            seated.append(p)
            total += p
            check = (check * 31 + p) % 1000000007
        else:
            i = next_random() % len(seated)
            seated[i], seated[-1] = seated[-1], seated[i]
            p = seated.pop()
            room.leave(p)
    return total, check


def main():
    s = -1
    show(10, [s, s, s, s, 4, s])
    show(1, [s])
    show(1, [s, 0, s])
    show(2, [s, s])
    show(3, [s, s, s])
    show(4, [s, s, s, s])
    show(5, [s, s, s, s])
    show(10, [s, s, s, 0, s])
    show(10, [s, s, s, s, 9, s])
    show(8, [s, s, s, 0, 7, s, s])
    show(1000000000, [s, s, s, s])
    big_total, big_check = random_room(1000000000, 2000)
    print(f"a room of 10^9 seats, 2000 random calls: seats sum to {big_total}, checksum {big_check}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        count = 1 + next_random() % 60
        t, c = random_room(n, count)
        total += t
        check = (check * 31 + c) % 1000000007
    print(f"300 random rooms: seats sum to {total}, checksum {check}")


main()
