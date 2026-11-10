# LeetCode #2102: Sequentially Ordinal Rank Tracker -- Python mirror of
# the ★ arm (rank_tracker.kara): a `Place` ordered so that greater is
# better, the places handed out in a min-heap (worst on top) and the rest
# in a max-heap (best on top, as negated `Place`s). Prints the same lines.
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
    """A place ordered the other way round, for a max-heap from heapq."""

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
        worst = heapq.heappop(self.served)
        heapq.heappush(self.waiting, Worse(worst))

    def get(self):
        best = heapq.heappop(self.waiting).place
        heapq.heappush(self.served, best)
        return best.name


def answers(ops):
    tracker = SORTracker()
    out = []
    for name, score in ops:
        if name == "":
            out.append(tracker.get())
        else:
            tracker.add(name, score)
    return out


seed = 2102


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def fresh_name(longest, letters, taken):
    while True:
        n = next_random() % longest + 1
        name = "".join(chr(ord("a") + next_random() % letters) for _ in range(n))
        if name not in taken:
            taken.add(name)
            return name


def fold(check, name):
    for b in name.encode():
        check = (check * 31 + b) % 1000000007
    return (check * 31 + 7) % 1000000007


examples = [
    [("bradford", 2), ("branford", 3), ("", 0), ("alps", 2), ("", 0), ("orland", 2), ("", 0), ("orlando", 3), ("", 0), ("alpine", 2), ("", 0), ("", 0)],
    [("c", 5), ("b", 5), ("a", 5), ("", 0), ("", 0), ("", 0)],
    [("m", 1), ("", 0), ("l", 2), ("", 0), ("k", 3), ("", 0), ("z", 100000), ("", 0)],
    [("solo", 7), ("", 0)],
]
for ops in examples:
    print("[" + ", ".join(answers(ops)) + "]")
gets = 0
check = 0
for rnd in range(3000):
    calls = next_random() % 30 + 1
    taken = set()
    ops = []
    added = 0
    asked = 0
    for _ in range(calls):
        if asked < added and next_random() % 2 == 0:
            ops.append(("", 0))
            asked += 1
        elif rnd % 2 == 0:
            name = fresh_name(3, 4, taken)
            ops.append((name, next_random() % 3 + 1))
            added += 1
        else:
            name = fresh_name(10, 26, taken)
            ops.append((name, wide_random() % 100000 + 1))
            added += 1
    for name in answers(ops):
        gets += 1
        check = fold(check, name)
print(f"3000 runs: {gets} gets, checksum {check}")
taken = set()
ops = []
for i in range(20000):
    ops.append((fresh_name(10, 26, taken), (i * 7919) % 1000 + 1))
    ops.append(("", 0))
got = answers(ops)
big = 0
for name in got:
    big = fold(big, name)
print(f"40000 calls: first {got[0]}, 10000th {got[9999]}, last {got[-1]}, checksum {big}")
