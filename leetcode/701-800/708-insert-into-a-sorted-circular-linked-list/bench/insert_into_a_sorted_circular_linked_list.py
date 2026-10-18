# LeetCode #708: Insert into a Sorted Circular Linked List -- an arena.
# Benchmark mirror of the Kara star arm: values and next links in two
# lists; walk from the given node to the first gap that fits.


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


def main():
    seed = 708

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    checksum = 0
    n = 20000
    for _ in range(5):
        for _ in range(10):
            values = []
            for _ in range(n):
                hi = next_random()
                lo = next_random()
                values.append((hi * 32768 + lo) % 2000001 - 1000000)
            values.sort()
            start = next_random() % n
            ring = Ring()
            for i in range(n):
                ring.vals.append(values[(start + i) % n])
                ring.next.append((i + 1) % n)
            head = 0
            for _ in range(1000):
                hi = next_random()
                lo = next_random()
                head = ring.insert(head, (hi * 32768 + lo) % 2000001 - 1000000)
            at = head
            while True:
                checksum = (checksum * 31 + ring.vals[at] + 1000001) % 1000000007
                at = ring.next[at]
                if at == head:
                    break
    print(f"5 rounds of 10 rings of 20000 values, 1000 inserts each: checksum {checksum}")


main()
