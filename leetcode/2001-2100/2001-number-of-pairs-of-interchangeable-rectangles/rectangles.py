# LeetCode #2001: Number of Pairs of Interchangeable Rectangles -- the
# mirror of the ★ arm, rectangles.kara; its output is byte-identical.
from math import gcd


def interchangeable(rectangles):
    seen = {}
    pairs = 0
    for w, h in rectangles:
        g = gcd(w, h)
        key = (w // g, h // g)
        before = seen.get(key, 0)
        pairs += before
        seen[key] = before + 1
    return pairs


seed = 2001


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` rectangles: each a multiple of one of `shapes` base ratios with sides
# up to `side`, or (when `shapes` is 0) sides drawn freely up to `side`.
def random_rectangles(n, shapes, side):
    bases = []
    for _ in range(shapes):
        bases.append((next_random() % 9 + 1, next_random() % 9 + 1))
    rects = []
    for _ in range(n):
        if shapes == 0:
            rects.append((next_random() % side + 1, next_random() % side + 1))
        else:
            w, h = bases[next_random() % shapes]
            m = next_random() % (side // max(w, h)) + 1
            rects.append((w * m, h * m))
    return rects


def mix(check, answer):
    return (check * 31 + answer % 1000003) % 1000000007


def show(rects):
    return "[" + ", ".join(f"({w}, {h})" for w, h in rects) + "]"


def main():
    examples = [
        [(4, 8), (3, 6), (10, 20), (15, 30)],
        [(4, 5), (7, 8)],
        [(1, 1)],
        [(2, 3), (3, 2)],
        [(1, 2), (2, 4), (3, 6), (4, 7)],
        [(6, 4), (9, 6), (3, 2), (12, 8), (5, 5), (7, 7)],
        [(100000, 99999), (99999, 100000), (100000, 100000)],
        [(100000, 1), (1, 100000), (100000, 1)],
    ]
    for rects in examples:
        print(f"{show(rects)} -> {interchangeable(rects)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        rects = random_rectangles(n, 0, next_random() % 6 + 1)
        answer = interchangeable(rects)
        total += answer
        check = mix(check, answer)
    print(f"3000 sets of 1 to 20 small rectangles: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        rects = random_rectangles(n, next_random() % 5 + 1, 60)
        answer = interchangeable(rects)
        total += answer
        check = mix(check, answer)
    print(f"3000 sets of 1 to 40 rectangles of 1 to 5 shapes: sum {total}, checksum {check}")
    total = check = 0
    for a in range(6):
        shapes = [0, 3, 20, 80, 0, 50][a]
        rects = random_rectangles(20000, shapes, 100000 if shapes == 0 else 30000)
        answer = interchangeable(rects)
        total += answer
        check = mix(check, answer)
    print(f"6 sets of 20000 rectangles: sum {total}, checksum {check}")
    same = [(7 * (i % 1000 + 1), 3 * (i % 1000 + 1)) for i in range(100000)]
    print(f"100000 rectangles of one shape: {interchangeable(same)}")


main()
