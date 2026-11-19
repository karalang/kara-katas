# LeetCode #1634: Add Two Polynomials Represented as Linked Lists -- the
# bench's Python mirror: the ★ arm on 10 random pairs of polynomials with
# powers below 400000, all drawn first as terms; each pair is built into
# two lists and added.


class PolyNode:
    __slots__ = ("coefficient", "power", "next")

    def __init__(self, coefficient=0, power=0, next=None):
        self.coefficient = coefficient
        self.power = power
        self.next = next


def add_poly(poly1, poly2):
    head = PolyNode()
    tail = head
    a, b = poly1, poly2
    while a is not None or b is not None:
        if a is not None and b is not None and a.power == b.power:
            coefficient, power = a.coefficient + b.coefficient, a.power
            a, b = a.next, b.next
        elif a is not None and b is not None and a.power < b.power:
            coefficient, power = b.coefficient, b.power
            b = b.next
        elif a is not None:
            coefficient, power = a.coefficient, a.power
            a = a.next
        else:
            coefficient, power = b.coefficient, b.power
            b = b.next
        if coefficient != 0:
            node = PolyNode(coefficient, power)
            tail.next = node
            tail = node
    return head.next


seed = 1634


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_terms(terms):
    head = None
    for coefficient, power in reversed(terms):
        head = PolyNode(coefficient, power, head)
    return head


def random_terms():
    terms = []
    for power in range(399999, -1, -1):
        if next_random() % 2 == 0:
            coefficient = next_random() % 6 - 3
            if coefficient >= 0:
                coefficient += 1
            terms.append((coefficient, power))
    return terms


def main():
    pairs = []
    for _ in range(10):
        poly1 = random_terms()
        poly2 = random_terms()
        pairs.append((poly1, poly2))
    check = 0
    terms = 0
    for poly1, poly2 in pairs:
        node = add_poly(from_terms(poly1), from_terms(poly2))
        while node is not None:
            terms += 1
            check = ((check * 31 + node.coefficient + 1000000) % 1000000007 * 31 + node.power) % 1000000007
            node = node.next
    print(f"10 pairs of up to 400000 terms: {terms} terms, checksum {check}")


main()
