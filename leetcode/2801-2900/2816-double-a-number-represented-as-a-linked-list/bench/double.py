# LeetCode #2816: Double a Number Represented as a Linked List -- the
# bench in Python: the ★ arm over 200 numbers of 10^4 digits, all drawn
# first, then each built as a list and doubled 20 times, the list read
# back after each.


class ListNode:
    __slots__ = ("val", "next")

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


seed = 2816


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 200, 20, 10000
    numbers = []
    for _ in range(count):
        digits = [next_random() % 10 for _ in range(n)]
        if digits[0] == 0:
            digits[0] = next_random() % 9 + 1
        numbers.append(digits)
    total = 0
    check = 0
    for r in range(rounds):
        for digits in numbers:
            node = double_it(build(digits))
            h = r
            while node is not None:
                total += node.val
                h = (h * 131 + node.val) % 1000000007
                node = node.next
            check = (check * 31 + h) % 1000000007
    print(f"{count} numbers of {n} digits, {rounds} rounds: digits sum to {total}, checksum {check}")


main()
