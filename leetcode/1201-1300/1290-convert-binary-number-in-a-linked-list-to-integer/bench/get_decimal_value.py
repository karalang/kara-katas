# LeetCode #1290 bench: the ★ arm over 10^4 lists of 30 nodes built once,
# then 500 passes, each setting one bit of every list and reading it back.


class ListNode:
    __slots__ = ("val", "next")

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


def set_bit(head, k, bit):
    cur = head
    i = 0
    while cur is not None:
        if i == k:
            cur.val = bit
            return
        i += 1
        cur = cur.next


def main():
    seed = 1290

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    heads = []
    for _ in range(10000):
        head = None
        for _ in range(30):
            head = ListNode(next_random() % 2, head)
        heads.append(head)
    check = 0
    for p in range(500):
        for a in range(len(heads)):
            set_bit(heads[a], (check + a) % 30, check // 16 % 2)
            check = (check * 31 + get_decimal_value(heads[a]) + p) % 1000000007
    print(f"500 passes over 10^4 lists of 30 bits: checksum {check}")


main()
