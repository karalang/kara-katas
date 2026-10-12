# Benchmark for #445: mirror of add_two_numbers.kara (two stacks) on 100
# random numbers of 1,000 to 2,000 digits, built once; 60 rounds add each
# to the next.


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


seed = 445


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100
    rounds = 60
    numbers = []
    for _ in range(count):
        length = 1000 + next_random() % 1001
        digits = []
        for i in range(length):
            d = 9 if next_random() % 2 == 0 else next_random() % 10
            if i == 0 and d == 0:
                d = 1
            digits.append(d)
        head = None
        for d in reversed(digits):
            head = ListNode(d, head)
        numbers.append(head)
    digits = 0
    checksum = 0
    for rnd in range(rounds):
        for i in range(count):
            node = add_two_numbers(numbers[i], numbers[(i + 1) % count])
            while node is not None:
                digits += 1
                checksum = (checksum * 31 + node.val + rnd) % 1000000007
                node = node.next
    print(f"{rounds} rounds on {count} numbers: {digits} digits, checksum {checksum}")


main()
