# LeetCode #1146: Snapshot Array -- the Python mirror of the ★ arm: a
# history of (snap, value) pairs for each place, the last pair at or
# before the snap asked found with bisect.
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


seed = 1146


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    n = 50000
    arr = SnapshotArray(n)
    total = check = 0
    for r in range(50000):
        for _ in range(50):
            i = wide() % n
            arr.set(i, wide() % 1000000001)
        arr.snap()
        for _ in range(50):
            i = wide() % n
            got = arr.get(i, wide() % (r + 1))
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"50000 rounds of 50 sets, a snap and 50 gets on 50000 places: gets total {total}, checksum {check}")


main()
