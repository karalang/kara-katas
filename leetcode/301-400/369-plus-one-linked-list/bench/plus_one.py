# Benchmark for #369 -- mirror of plus_one.kara.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt):
        self.val = val
        self.next = nxt


def plus_one(head):
    front = ListNode(0, head)
    last = front
    at = front.next
    while at is not None:
        if at.val != 9:
            last = at
        at = at.next
    last.val += 1
    rest = last.next
    while rest is not None:
        rest.val = 0
        rest = rest.next
    return front if front.val == 1 else front.next


def main():
    seed = 369
    total = 0
    checksum = 0
    for i in range(20):
        head = None
        for k in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            d = 9 if i % 2 == 0 and k < 50000 else (seed // 65536) % 10
            head = ListNode(1 if k == 99999 and d == 0 else d, head)
        for _ in range(20):
            head = plus_one(head)
        at = head
        while at is not None:
            total += 1
            checksum = (checksum * 31 + at.val) % 1000000007
            at = at.next
    print(f"{total} digits, checksum {checksum}")


main()
