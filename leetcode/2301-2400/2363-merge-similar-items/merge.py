# LeetCode #2363: Merge Similar Items -- the Python mirror of the ★ arm:
# every item of both lists added into a map from value to total weight,
# which is walked in order of value.


def merge_similar_items(items1, items2):
    totals = {}
    for value, weight in items1 + items2:
        totals[value] = totals.get(value, 0) + weight
    return [[value, totals[value]] for value in sorted(totals)]


SEED = [2363]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def show(items):
    return "[" + ",".join(f"[{p[0]},{p[1]}]" for p in items) + "]"


def random_items(count, values):
    # count distinct values from 1 to values, each with a weight of 1 to 1000
    used = [False] * (values + 1)
    items = []
    while len(items) < count:
        v = 1 + next_random() % values
        if not used[v]:
            used[v] = True
            items.append([v, 1 + next_random() % 1000])
    return items


def main():
    # LeetCode's three examples; one item in each list with the same
    # value; 1000 items each with every value; then 2000 random pairs of
    # lists of 1 to 30 items with values from 1 to 1 to 60
    print(show(merge_similar_items([[1, 1], [4, 5], [3, 8]], [[3, 1], [1, 5]])))
    print(show(merge_similar_items([[1, 1], [3, 2], [2, 3]], [[2, 1], [3, 2], [1, 3]])))
    print(show(merge_similar_items([[1, 3], [2, 2]], [[7, 1], [2, 2], [1, 4]])))
    print(show(merge_similar_items([[1000, 1000]], [[1000, 1000]])))
    big = merge_similar_items([[v, v] for v in range(1000, 0, -1)], [[v, v % 7 + 1] for v in range(1, 1001)])
    total = sum(p[0] * p[1] for p in big)
    print(f"{len(big)} values, {total}")
    check = 0
    shared = 0
    for _ in range(2000):
        values = 1 + next_random() % 60
        n = 1 + next_random() % min(values, 30)
        m = 1 + next_random() % min(values, 30)
        items1 = random_items(n, values)
        items2 = random_items(m, values)
        merged = merge_similar_items(items1, items2)
        for p in merged:
            check = (check * 31 + p[0] * 1009 + p[1]) % 1000000007
        check = (check * 31 + len(merged)) % 1000000007
        shared += n + m - len(merged)
    print(f"2000 pairs: checksum {check}, {shared} values in both")


if __name__ == "__main__":
    main()
