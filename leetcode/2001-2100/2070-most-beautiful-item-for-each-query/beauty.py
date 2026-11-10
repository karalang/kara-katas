# LeetCode #2070: Most Beautiful Item for Each Query -- the Python mirror
# of beauty.kara (the ★ arm): the items sorted by price, the best beauty of
# each prefix beside them, and each query's prefix found by binary search.
from bisect import bisect_right


def maximum_beauty(items, queries):
    ordered = sorted(items, key=lambda item: item[0])
    prices = [item[0] for item in ordered]
    best = []
    most = 0
    for item in ordered:
        most = max(most, item[1])
        best.append(most)
    out = []
    for q in queries:
        end = bisect_right(prices, q)
        out.append(0 if end == 0 else best[end - 1])
    return out


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def up_to(top, seed):
    a = next_random(seed)
    b = next_random(seed)
    return (a * 32768 + b) % top + 1


def items_of(n, top, seed):
    items = []
    for _ in range(n):
        price = up_to(top, seed)
        items.append([price, up_to(top, seed)])
    return items


def queries_of(m, top, seed):
    return [up_to(top, seed) for _ in range(m)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def checksum(answers):
    check = 0
    for a in answers:
        check = (check * 31 + a) % 1000000007
    return check


def main():
    examples = [
        ([[1, 2], [3, 2], [2, 4], [5, 6], [3, 5]], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [1, 2], [1, 3], [1, 4]], [1]),
        ([[10, 1000]], [5]),
        ([[5, 1], [5, 9], [7, 3]], [4, 5, 6, 7, 1000000000]),
        ([[1000000000, 1000000000], [1, 1]], [999999999, 1000000000]),
    ]
    for items, queries in examples:
        print(f"{len(items)} items, {show(queries)} -> {show(maximum_beauty(items, queries))}")
    seed = [2070]
    check = 0
    for _ in range(300):
        n = next_random(seed) % 50 + 1
        m = next_random(seed) % 50 + 1
        top = [10, 1000, 1000000000][next_random(seed) % 3]
        items = items_of(n, top, seed)
        queries = queries_of(m, top, seed)
        check = (check * 31 + checksum(maximum_beauty(items, queries))) % 1000000007
    print(f"300 shops: checksum {check}")
    items = items_of(100000, 1000000000, seed)
    queries = queries_of(100000, 1000000000, seed)
    answers = maximum_beauty(items, queries)
    print(f"100000 items, 100000 queries: checksum {checksum(answers)}, sum {sum(answers)}")


main()
