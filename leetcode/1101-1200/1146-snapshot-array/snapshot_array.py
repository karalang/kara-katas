# LeetCode #1146: Snapshot Array -- the Python mirror of the ★ arm: a
# history of (snap, value) pairs for each place, the last pair at or
# before the snap asked found by binary search.
from bisect import bisect_right


class SnapshotArray:
    def __init__(self, length):
        self.history = [[(0, 0)] for _ in range(length)]
        self.snaps = 0

    def set(self, index, val):
        h = self.history[index]
        if h[-1][0] == self.snaps:
            h[-1] = (self.snaps, val)
        else:
            h.append((self.snaps, val))

    def snap(self):
        self.snaps += 1
        return self.snaps - 1

    def get(self, index, snap_id):
        h = self.history[index]
        return h[bisect_right(h, snap_id, key=lambda p: p[0]) - 1][1]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def pick(bound):
    return next_random() % bound


def value():
    if next_random() % 3 == 0:
        return pick(5)
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % 1000000001


def session(length, calls, snaps):
    arr = SnapshotArray(length)
    taken = total = check = 0
    for _ in range(calls):
        r = next_random() % snaps
        if r == 0 or (taken == 0 and r % 2 == 0):
            i = arr.snap()
            taken += 1
            check = (check * 31 + i + 1) % 1000000007
        elif r % 2 == 1 or taken == 0:
            i = pick(length)
            arr.set(i, value())
        else:
            i = pick(length)
            got = arr.get(i, pick(taken))
            total += got
            check = (check * 31 + got) % 1000000007
    return total, check


def main():
    global seed
    arr = SnapshotArray(3)
    arr.set(0, 5)
    print(f"snap() = {arr.snap()}")
    arr.set(0, 6)
    print(f"get(0, 0) = {arr.get(0, 0)}")
    print(f"get(2, 0) = {arr.get(2, 0)}")
    arr.set(1, 7)
    arr.set(1, 8)
    print(f"snap() = {arr.snap()}")
    print(f"snap() = {arr.snap()}")
    arr.set(1, 9)
    arr.set(0, 0)
    print(f"snap() = {arr.snap()}")
    print(f"get(1, 1) = {arr.get(1, 1)}, get(1, 2) = {arr.get(1, 2)}, get(1, 3) = {arr.get(1, 3)}")
    print(f"get(0, 0) = {arr.get(0, 0)}, get(0, 2) = {arr.get(0, 2)}, get(0, 3) = {arr.get(0, 3)}")
    print(f"get(1, 0) = {arr.get(1, 0)}")
    one = SnapshotArray(1)
    for v in range(1, 6):
        one.set(0, v * 10)
        one.snap()
    print("one place, snaps 0 to 4: " + " ".join(str(one.get(0, s)) for s in range(5)))
    seed = 1146
    total = check = 0
    for s in range(2000):
        length = 1 + next_random() % 20
        calls = 1 + next_random() % 60
        t, c = session(length, calls, 3 if s % 2 == 0 else 10)
        total += t
        check = (check * 31 + c) % 1000000007
    print(f"2000 random sessions: gets total {total}, checksum {check}")
    n = 50000
    wide = SnapshotArray(n)
    for i in range(24999):
        wide.set(i, i * 3)
    wide.snap()
    print(f"50000 places, half set once: gets total {sum(wide.get(i, 0) for i in range(25000))}")
    deep = SnapshotArray(n)
    for v in range(12500):
        deep.set(0, v + 1)
        deep.snap()
    print(f"one place snapped 12500 times: gets total {sum(deep.get(0, s * 50) for s in range(250))}")
    t, c = session(50000, 50000, 100)
    print(f"50000 random calls on 50000 places: gets total {t}, checksum {c}")


main()
