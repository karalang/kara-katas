# LeetCode #445: Add Two Numbers II -- mirror of add_two_numbers.kara
# (two stacks).


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    a = []
    node = l1
    while node is not None:
        a.append(node.val)
        node = node.next
    b = []
    node = l2
    while node is not None:
        b.append(node.val)
        node = node.next
    total = None
    carry = 0
    while a or b or carry > 0:
        digit = carry
        if a:
            digit += a.pop()
        if b:
            digit += b.pop()
        total = ListNode(digit % 10, total)
        carry = digit // 10
    return total


def from_digits(digits):
    head = None
    for d in reversed(digits):
        head = ListNode(d, head)
    return head


def to_string(head):
    parts = []
    node = head
    while node is not None:
        parts.append(str(node.val))
        node = node.next
    return "[" + ",".join(parts) + "]"


def show(a, b):
    l1 = from_digits(a)
    l2 = from_digits(b)
    total = add_two_numbers(l1, l2)
    print(f"{to_string(l1)} + {to_string(l2)} = {to_string(total)}")


seed = 445


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_digits():
    length = 1 + next_random() % 100
    digits = []
    for i in range(length):
        d = 9 if next_random() % 2 == 0 else next_random() % 10
        if i == 0 and length > 1 and d == 0:
            d = 1
        digits.append(d)
    return digits


show([7, 2, 4, 3], [5, 6, 4])
show([2, 4, 3], [5, 6, 4])
show([0], [0])
show([9, 9, 9, 9], [1])
show([1], [9, 9, 9])
show([5], [5])
show([1, 0, 0, 0], [0])
show([8, 9, 9, 9, 9, 5], [4, 6])
count = 300
digits = 0
checksum = 0
for _ in range(count):
    l1 = from_digits(random_digits())
    l2 = from_digits(random_digits())
    node = add_two_numbers(l1, l2)
    while node is not None:
        digits += 1
        checksum = (checksum * 31 + node.val) % 1000000007
        node = node.next
print(f"{count} random sums: {digits} digits, checksum {checksum}")
