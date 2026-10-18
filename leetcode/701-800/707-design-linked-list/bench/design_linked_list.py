# LeetCode #707: Design Linked List -- singly linked, with a sentinel.
# Benchmark mirror of the Kara star arm: walk to the node before the
# position, then link a new node in after it or link past the next.


class Node:
    __slots__ = ("val", "next")

    def __init__(self, val, next):
        self.val = val
        self.next = next


class MyLinkedList:
    def __init__(self):
        self.head = Node(0, None)
        self.size = 0

    def before(self, index):
        at = self.head
        for _ in range(index):
            at = at.next
        return at

    def get(self, index):
        if index < 0 or index >= self.size:
            return -1
        return self.before(index).next.val

    def add_at_head(self, val):
        self.add_at_index(0, val)

    def add_at_tail(self, val):
        self.add_at_index(self.size, val)

    def add_at_index(self, index, val):
        if index < 0 or index > self.size:
            return
        prev = self.before(index)
        prev.next = Node(val, prev.next)
        self.size += 1

    def delete_at_index(self, index):
        if index < 0 or index >= self.size:
            return
        prev = self.before(index)
        prev.next = prev.next.next
        self.size -= 1


def main():
    seed = 707

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    values = 0
    checksum = 0
    for _ in range(5):
        for _ in range(10):
            lst = MyLinkedList()
            for _ in range(6000):
                op = next_random() % 5
                index = next_random() % (lst.size + 3)
                val = next_random() % 1001
                if op == 0:
                    checksum = (checksum * 31 + lst.get(index) + 2) % 1000000007
                elif op == 1:
                    lst.add_at_head(val)
                elif op == 2:
                    lst.add_at_tail(val)
                elif op == 3:
                    lst.add_at_index(index, val)
                else:
                    lst.delete_at_index(index)
            values += lst.size
    print(f"5 rounds of 10 lists of 6000 calls: {values} values left, checksum {checksum}")


main()
