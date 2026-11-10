# LeetCode #2080: Range Frequency Queries -- Python mirror of the ★ arm
# (frequency.kara): every value's places in order in a dict, and a query's
# count the places before `right + 1` less those before `left`, by binary
# search.
from bisect import bisect_left, bisect_right


class RangeFreqQuery:
    def __init__(self, arr):
        self.places = {}
        for i, v in enumerate(arr):
            self.places.setdefault(v, []).append(i)

    def query(self, left, right, value):
        at = self.places.get(value)
        if at is None:
            return 0
        return bisect_right(at, right) - bisect_left(at, left)


seed = 2080


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def answers(arr, queries):
    rfq = RangeFreqQuery(arr)
    return [rfq.query(l, r, v) for l, r, v in queries]


examples = [
    ([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56], [(1, 2, 4), (0, 11, 33)]),
    ([1], [(0, 0, 1), (0, 0, 2)]),
    ([5, 5, 5, 5], [(0, 3, 5), (1, 2, 5), (3, 3, 5), (0, 3, 4)]),
    ([1, 2, 1, 2, 1, 2], [(0, 5, 1), (1, 4, 2), (2, 2, 2), (5, 5, 2)]),
    ([7, 1, 7, 1, 7], [(0, 4, 7), (1, 3, 7), (0, 0, 1), (4, 4, 7)]),
]
for arr, queries in examples:
    qs = ",".join(f"({l},{r},{v})" for l, r, v in queries)
    print(f"{show(arr)}, [{qs}] -> {show(answers(arr, queries))}")
total = 0
check = 0
for _ in range(300):
    n = next_random() % 200 + 1
    top = [3, 30, 10000][next_random() % 3]
    arr = [next_random() % top + 1 for _ in range(n)]
    queries = []
    for _ in range(50):
        a = next_random() % n
        b = next_random() % n
        if next_random() % 2 == 0:
            value = arr[next_random() % n]
        else:
            value = next_random() % (top + 1) + 1
        queries.append((min(a, b), max(a, b), value))
    for a in answers(arr, queries):
        total += a
        check = (check * 31 + a) % 1000000007
print(f"300 arrays: sum {total}, checksum {check}")
arr = [next_random() % 100 + 1 for _ in range(100000)]
queries = []
for _ in range(200):
    a = next_random() % 50000
    b = 50000 + next_random() % 50000
    queries.append((a, b, next_random() % 100 + 1))
big = answers(arr, queries)
print(f"100000 values, 200 queries: sum {sum(big)}")
