"""LeetCode #328: Odd Even Linked List — Python mirror.

Mirrors odd_even_list.kara: nodes relinked in place with two tails, `odd`
and `even`, and the even group hung after the last odd node. Prints the
same lines.
"""


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def odd_even_list(head):
    if head is None or head.next is None:
        return head
    first, second = head, head.next
    odd, even = first, second
    while even.next is not None:
        n = even.next
        odd.next = n
        odd = n
        even.next = n.next
        if n.next is None:
            break
        even = n.next
    odd.next = second
    return first


def from_vec(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_vec(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def report(values):
    got = to_vec(odd_even_list(from_vec(values)))
    print(f"{values} -> {got}")


seed = 328


def next_rand():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    report([1, 2, 3, 4, 5])
    report([2, 1, 3, 5, 6, 4, 7])

    report([])
    report([1])
    report([1, 2])
    report([1, 2, 3])
    report([7, 7, 7, 7])
    report([-1, 0, -1, 0, -1, 0])

    for n in [10, 11, 1000, 1001, 10000]:
        values = list(range(1, n + 1))
        got = to_vec(odd_even_list(from_vec(values)))
        s = 0
        for k, v in enumerate(got, 1):
            s = (s * 31 + v * k) % 1000000007
        print(f"n={n}: first {got[0]}, first even {got[(n + 1) // 2]}, last {got[n - 1]}, hash {s}")

    for _ in range(3):
        n = next_rand() % 9 + 1
        values = [next_rand() % 100 for _ in range(n)]
        report(values)


main()
