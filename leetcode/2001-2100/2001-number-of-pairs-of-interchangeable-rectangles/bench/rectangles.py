# LeetCode #2001: Number of Pairs of Interchangeable Rectangles -- the
# benchmark, the same algorithm as rectangles.kara.
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


def main():
    calls = total = check = 0
    for a in range(20):
        shapes = [10, 100, 1000, 10000][a % 4]
        bases = [(next_random() % 300 + 1, next_random() % 300 + 1) for _ in range(shapes)]
        rects = []
        for _ in range(100000):
            w, h = bases[next_random() % shapes]
            m = next_random() % (100000 // max(w, h)) + 1
            rects.append((w * m, h * m))
        for _ in range(10):
            answer = interchangeable(rects)
            total += answer
            check = (check * 31 + answer % 1000003) % 1000000007
            calls += 1
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
