# LeetCode #2816: Double a Number Represented as a Linked List -- the
# Python mirror of the ★ arm: a 0 node put in front when the first digit
# is 5 or more, then each digit doubled in place, plus one when the next
# digit is 5 or more.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def double_it(head):
    if head.val > 4:
        head = ListNode(0, head)
    node = head
    while node is not None:
        node.val = node.val * 2 % 10
        if node.next is not None and node.next.val > 4:
            node.val += 1
        node = node.next
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


def doubled(values):
    return values_of(double_it(build(values)))


seed = 2816


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x) % 1000000007
    return h


def random_digits(n):
    digits = [next_random() % 10 for _ in range(n)]
    if n > 1 and digits[0] == 0:
        digits[0] = next_random() % 9 + 1
    return digits


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    print(show(doubled([1, 8, 9])))
    print(show(doubled([9, 9, 9])))
    print(show(doubled([0])))
    nines = doubled([9] * 10000)
    print(f"{len(nines)} {digest(nines)}")
    fours = doubled([4] * 10000)
    print(f"{len(fours)} {digest(fours)}")
    for count, label in ((3000, "short"), (50, "long")):
        check = 0
        longer = 0
        for _ in range(count):
            if label == "short":
                n = next_random() % 12 + 1
            else:
                a = next_random()
                n = (a * 32768 + next_random()) % 10000 + 1
            out = doubled(random_digits(n))
            longer += len(out) - n
            check = (check * 31 + digest(out)) % 1000000007
        print(f"{count} {label} numbers: {longer} grew a digit, checksum {check}")


main()
