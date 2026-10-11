# LeetCode #369: Plus One Linked List -- mirror of plus_one.kara.


class ListNode:
    def __init__(self, val, nxt=None):
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


def from_digits(digits):
    head = None
    for d in reversed(digits):
        head = ListNode(d, head)
    return head


def to_text(node):
    out = []
    while node is not None:
        out.append(str(node.val))
        node = node.next
    return "".join(out)


def show(label, digits):
    print(f"{label}: {to_text(plus_one(from_digits(digits)))}")


def main():
    show("example 1", [1, 2, 3])
    show("example 2", [0])
    show("one nine", [9])
    show("all nines", [9, 9, 9])
    show("trailing nines", [1, 9, 9])
    show("a carry that stops at an 8", [8, 9, 9, 9])
    show("zeros before the last digit", [1, 0, 0])
    show("a nine before the last digit", [9, 0])
    show("sixty nines", [9] * 60)
    seed = 369
    total = 0
    checksum = 0
    for i in range(500):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 30
        digits = []
        for k in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            d = (seed // 65536) % 10
            if i % 2 == 0 and k >= n // 2:
                digits.append(9)
            elif k == 0 and n > 1 and d == 0:
                digits.append(1)
            else:
                digits.append(d)
        text = to_text(plus_one(from_digits(digits)))
        total += len(text)
        for ch in text:
            checksum = (checksum * 31 + int(ch)) % 1000000007
    print(f"500 random numbers: {total} digits, checksum {checksum}")


main()
