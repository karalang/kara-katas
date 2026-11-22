# LeetCode #2807: Insert Greatest Common Divisors in Linked List -- the
# Python mirror of the ★ arm: one walk, a node with the gcd of each pair
# linked between them in place.


class ListNode:
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


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def values_of(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def inserted(values):
    return values_of(insert_greatest_common_divisors(build(values)))


seed = 2807


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x) % 1000000007
    return h


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    print(show(inserted([18, 6, 10, 3])))
    print(show(inserted([7])))
    same = inserted([1000] * 5000)
    print(f"{len(same)} {digest(same)}")
    counting = inserted([v % 1000 + 1 for v in range(1, 5001)])
    print(f"{len(counting)} {digest(counting)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        out = inserted([next_random() % 30 + 1 for _ in range(n)])
        total += sum(out)
        check = (check * 31 + digest(out)) % 1000000007
    print(f"3000 short lists: values sum to {total}, checksum {check}")
    total = 0
    check = 0
    for t in range(50):
        n = next_random() % 5000 + 1
        step = 12 if t % 2 == 0 else 1
        out = inserted([(next_random() % (1000 // step) + 1) * step for _ in range(n)])
        total += sum(out)
        check = (check * 31 + digest(out)) % 1000000007
    print(f"50 long lists: values sum to {total}, checksum {check}")


main()
