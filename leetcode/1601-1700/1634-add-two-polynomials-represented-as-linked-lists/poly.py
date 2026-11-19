# LeetCode #1634: Add Two Polynomials Represented as Linked Lists -- the
# Python mirror of the ★ arm: both lists merged in one walk from the
# highest power down, equal powers added, a sum of 0 left out.


class PolyNode:
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


# ---- the harness: the same as every arm's ---------------------------------

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


def to_terms(poly):
    terms = []
    while poly is not None:
        terms.append([poly.coefficient, poly.power])
        poly = poly.next
    return terms


def random_terms(most, powers, spread):
    count = min(next_random() % (most + 1), powers)
    chosen = set()
    while len(chosen) < count:
        chosen.add(next_random() % powers)
    terms = []
    for power in sorted(chosen, reverse=True):
        coefficient = next_random() % (2 * spread) - spread
        if coefficient >= 0:
            coefficient += 1
        terms.append([coefficient, power])
    return terms


def batch(count, most, powers, spread):
    check = 0
    terms = 0
    total = 0
    for _ in range(count):
        poly1 = random_terms(most, powers, spread)
        poly2 = random_terms(most, powers, spread)
        for c, p in to_terms(add_poly(from_terms(poly1), from_terms(poly2))):
            terms += 1
            total += c
            check = ((check * 31 + c + 1000000) % 1000000007 * 31 + p) % 1000000007
    print(f"{count} pairs of up to {most} terms: {terms} terms, coefficients sum to {total}, checksum {check}")


def show(poly1, poly2):
    terms = to_terms(add_poly(from_terms(poly1), from_terms(poly2)))
    print("[" + ", ".join(f"[{c}, {p}]" for c, p in terms) + "]")


show([[1, 1]], [[1, 0]])
show([[2, 2], [4, 1], [3, 0]], [[3, 2], [-4, 1], [-1, 0]])
show([[1, 2]], [[-1, 2]])
show([], [])
show([[5, 3], [1, 0]], [])
show([[1, 4], [2, 2], [3, 1]], [[-1, 3], [-2, 2], [7, 0]])
batch(3000, 5, 8, 3)
batch(300, 50, 100, 1000)
batch(5, 5000, 10000, 5)
