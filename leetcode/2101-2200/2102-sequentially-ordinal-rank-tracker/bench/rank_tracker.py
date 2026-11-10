# LeetCode #2102: Sequentially Ordinal Rank Tracker -- Python mirror of the
# ★ arm's benchmark (rank_tracker.kara): the same 20 runs of 4 * 10^4
# calls, two heaps of a Place ordered so that greater is better.
import heapq


class Place:
    __slots__ = ("score", "name")

    def __init__(self, score, name):
        self.score = score
        self.name = name

    def __lt__(self, other):  # worse than
        if self.score != other.score:
            return self.score < other.score
        return self.name > other.name


class Worse:
    __slots__ = ("place",)

    def __init__(self, place):
        self.place = place

    def __lt__(self, other):
        return other.place < self.place


class SORTracker:
    def __init__(self):
        self.served = []
        self.waiting = []

    def add(self, name, score):
        heapq.heappush(self.served, Place(score, name))
        heapq.heappush(self.waiting, Worse(heapq.heappop(self.served)))

    def get(self):
        best = heapq.heappop(self.waiting).place
        heapq.heappush(self.served, best)
        return best.name


seed = 2102


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


gets = 0
check = 0
for _ in range(20):
    taken = set()
    tracker = SORTracker()
    added = 0
    asked = 0
    while asked < 20000:
        if added < 20000 and (asked == added or next_random() % 2 == 0):
            while True:
                n = next_random() % 10 + 1
                name = "".join(chr(97 + next_random() % 26) for _ in range(n))
                if name not in taken:
                    taken.add(name)
                    break
            tracker.add(name, wide_random() % 100000 + 1)
            added += 1
        else:
            name = tracker.get()
            asked += 1
            gets += 1
            for b in name.encode():
                check = (check * 31 + b) % 1000000007
            check = (check * 31 + 7) % 1000000007
print(f"20 runs: {gets} gets, checksum {check}")
