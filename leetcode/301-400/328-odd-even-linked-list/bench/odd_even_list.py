"""Benchmark workload for LeetCode #328 — Python mirror of odd_even_list.kara.

Same workload: a list of LEN nodes built once, then PUNCHES punches, each
regrouping the list in place and walking it once to fold a rolling hash and
replace one value.
"""

LEN = 1000000
PUNCHES = 10
MODULUS = 1073741789


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next):
        self.val = val
        self.next = next


def odd_even_list(head):
    if head is None or head.next is None:
        return head
    first, second = head, head.next
    odd, even = first, second
    while True:
        n = even.next
        if n is None:
            break
        odd.next = n
        odd = n
        even.next = n.next
        if n.next is None:
            break
        even = n.next
    odd.next = second
    return first


seed = 328


def next_rand():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    head = None
    for _ in range(LEN):
        hi = next_rand()
        lo = next_rand()
        head = ListNode((hi * 32768 + lo) % 1000000, head)
    sink = 0
    for _ in range(PUNCHES):
        head = odd_even_list(head)
        hi = next_rand()
        lo = next_rand()
        pos = (hi * 32768 + lo) % LEN
        hi = next_rand()
        lo = next_rand()
        fresh = (hi * 32768 + lo) % 1000000
        k = 0
        n = head
        while n is not None:
            if k == pos:
                n.val = fresh
            sink = (sink * 31 + n.val * (k + 1)) % MODULUS
            n = n.next
            k += 1
    print(f"sink {sink}")


main()
