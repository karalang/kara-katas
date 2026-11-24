# LeetCode #1290: Convert Binary Number in a Linked List to Integer -- Python
# mirror of the ★ arm: one walk, the value so far doubled and the bit added.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def get_decimal_value(head):
    value = 0
    cur = head
    while cur is not None:
        value = value * 2 + cur.val
        cur = cur.next
    return value


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def main():
    print(f"{get_decimal_value(from_values([1, 0, 1]))} {get_decimal_value(from_values([0]))} {get_decimal_value(from_values([1]))} {get_decimal_value(from_values([0, 0, 0, 1]))}")
    ones = [1] * 30
    alternate = [(k + 1) % 2 for k in range(30)]
    print(f"{get_decimal_value(from_values(ones))} {get_decimal_value(from_values(alternate))}")
    seed = [1290]
    total = 0
    check = 0
    for k in range(20000):
        n = k + 1 if k < 30 else next_random(seed) % 30 + 1
        values = []
        for i in range(n):
            values.append(1 if i == 0 and n > 1 else next_random(seed) % 2)
        value = get_decimal_value(from_values(values))
        total += value
        check = (check * 131 + value) % 1000000007
    print(f"20000 random lists of 1 to 30 bits: total {total}, checksum {check}")


main()
