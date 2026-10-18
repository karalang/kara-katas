# LeetCode #708: Insert into a Sorted Circular Linked List -- an arena.
#
# A mirror of insert_into_a_sorted_circular_linked_list.kara (the ★ arm)
# and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fits(a, b, x):
    if a <= b:
        return a <= x <= b
    return x >= a or x <= b


class Ring:
    def __init__(self):
        self.vals = []
        self.next = []

    def insert(self, head, insert_val):
        node = len(self.vals)
        self.vals.append(insert_val)
        if head is None:
            self.next.append(node)
            return node
        prev = head
        while True:
            curr = self.next[prev]
            if fits(self.vals[prev], self.vals[curr], insert_val):
                break
            prev = curr
            if prev == head:
                break
        self.next.append(self.next[prev])
        self.next[prev] = node
        return head


class CircularList:
    def __init__(self, vals):
        n = len(vals)
        self.ring = Ring()
        for i in range(n):
            self.ring.vals.append(vals[i])
            self.ring.next.append((i + 1) % n)
        self.head = None if n == 0 else 0

    def insert(self, insert_val):
        self.head = self.ring.insert(self.head, insert_val)

    def values(self):
        out = []
        if self.head is not None:
            at = self.head
            while True:
                out.append(self.ring.vals[at])
                at = self.ring.next[at]
                if at == self.head:
                    break
        return out


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(vals, inserts):
    lst = CircularList(list(vals))
    for x in inserts:
        lst.insert(x)
    print(f"{fmt(vals)} insert {fmt(inserts)}: {fmt(lst.values())}")


def random_ring(n, lo, span):
    vals = sorted(lo + next_random() % (span + 1) for _ in range(n))
    start = 0 if n == 0 else next_random() % n
    return [vals[(start + i) % n] for i in range(n)]


def checksum(vals):
    s = 0
    for v in vals:
        s = (s * 31 + v + 1000001) % 1000000007
    return s


def main():
    global seed
    show([3, 4, 1], [2])
    show([], [1])
    show([1], [0])
    show([3, 5, 1], [6, 0, 3, 5, 1])
    show([1, 1, 3], [1, 3, 2])
    show([3, 3, 3], [3, 5, 1])
    show([7], [7, 7, 6, 8])
    show([-1000000, 1000000], [0, -1000000, 1000000])
    seed = 708
    for _ in range(2):
        lst = CircularList([])
        for _ in range(2000):
            lst.insert(next_random() % 2000001 - 1000000)
        vals = lst.values()
        print(f"2000 inserted: first {vals[0]}, checksum {checksum(vals)}")
    lst = CircularList(random_ring(50000, -1000000, 2000000))
    for _ in range(50):
        lst.insert(next_random() % 2000001 - 1000000)
    print(f"50000 nodes and 50 inserted: checksum {checksum(lst.values())}")
    total = 0
    for _ in range(300):
        n = next_random() % 31
        span = 5 if next_random() % 2 == 0 else 1000
        lst = CircularList(random_ring(n, -3, span))
        k = 1 + next_random() % 5
        for _ in range(k):
            lst.insert(next_random() % (span + 7) - 6)
        total = (total * 31 + checksum(lst.values())) % 1000000007
    print(f"300 random rings: checksum {total}")


main()
