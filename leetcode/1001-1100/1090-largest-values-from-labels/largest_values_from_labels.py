# LeetCode #1090: Largest Values From Labels -- Python mirror of the ★ arm.
def largest_vals_from_labels(values, labels, num_wanted, use_limit):
    items = sorted(zip(values, labels), key=lambda p: -p[0])
    used = {}
    taken = 0
    total = 0
    for value, label in items:
        if taken == num_wanted:
            break
        uses = used.get(label, 0)
        if uses < use_limit:
            used[label] = uses + 1
            total += value
            taken += 1
    return total

class Rng:
    def __init__(self, s): self.s = s
    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s // 65536

def show(xs): return "[" + ", ".join(str(x) for x in xs) + "]"

def main():
    cases = [
        ([5, 4, 3, 2, 1], [1, 1, 2, 2, 3], 3, 1),
        ([5, 4, 3, 2, 1], [1, 3, 3, 3, 2], 3, 2),
        ([9, 8, 8, 7, 6], [0, 0, 0, 1, 1], 3, 1),
        ([9, 8, 8, 7, 6], [0, 0, 0, 1, 1], 3, 2),
        ([7], [4], 1, 1),
        ([0, 0, 0], [1, 2, 3], 2, 1),
        ([3, 3, 3, 3], [1, 1, 1, 1], 4, 2),
        ([3, 3, 3, 3], [1, 1, 1, 1], 1, 4),
        ([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], 6, 1),
        ([10, 9, 8, 7, 6, 5], [1, 1, 2, 2, 3, 3], 4, 1),
        ([2, 6, 1, 2, 6], [2, 2, 2, 1, 1], 1, 1),
        ([4, 4, 4, 9, 2, 8], [0, 1, 0, 2, 1, 2], 5, 1),
    ]
    for v, l, w, u in cases:
        print(f"{show(v)} {show(l)} {w} {u} -> {largest_vals_from_labels(v, l, w, u)}")
    r = Rng(1090); h = 0; total = 0
    for _ in range(2000):
        n = r.next() % 20 + 1
        v = []; l = []
        for _ in range(n):
            v.append(r.next() % 21); l.append(r.next() % 6)
        w = r.next() % n + 1; u = r.next() % n + 1
        a = largest_vals_from_labels(v, l, w, u)
        total += a; h = (h * 31 + a) % 1000000007
    print(f"2000 random problems: answers sum to {total}, checksum {h}")
    v = []; l = []
    for _ in range(20000):
        v.append(r.next() % 20001); l.append(r.next() % 20001)
    print(f"20000 items: {largest_vals_from_labels(v, l, 20000, 1)}, {largest_vals_from_labels(v, l, 5000, 3)}, {largest_vals_from_labels(v, l, 100, 1)}")

main()
