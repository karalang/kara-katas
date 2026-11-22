# LeetCode #2807: Insert Greatest Common Divisors in Linked List -- the
# bench in Python: the ★ arm over 200 lists of 5000 values up to 1000, all
# drawn first, then each built afresh and answered 10 times.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def insert_greatest_common_divisors(head):
    cur = head
    while cur is not None:
        after = cur.next
        if after is None:
            break
        cur.next = ListNode(gcd(cur.val, after.val), after)
        cur = after
    return head


seed = 2807


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 200
    rounds = 10
    cases = []
    for t in range(count):
        step = 12 if t % 2 == 0 else 1
        cases.append([(next_random() % (1000 // step) + 1) * step for _ in range(5000)])
    total = 0
    check = 0
    for r in range(rounds):
        for values in cases:
            head = None
            for v in reversed(values):
                head = ListNode(v, head)
            cur = insert_greatest_common_divisors(head)
            s = 0
            while cur is not None:
                s += cur.val
                cur = cur.next
            total += s
            check = (check * 31 + s + r) % 1000000007
    print(f"{count} lists of 5000, {rounds} rounds: values sum to {total}, checksum {check}")


main()
