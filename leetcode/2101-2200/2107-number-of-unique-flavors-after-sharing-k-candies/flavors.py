# LeetCode #2107: Number of Unique Flavors After Sharing K Candies --
# Python mirror of flavors.kara: a dict of the kept flavors' counts, the
# first k candies taken out, the shared window sliding right one candy at
# a time. O(n).


def share_candies(candies, k):
    kept = {}
    for c in candies:
        kept[c] = kept.get(c, 0) + 1
    for c in candies[:k]:
        kept[c] -= 1
    distinct = sum(1 for n in kept.values() if n > 0)
    best = distinct
    for i in range(k, len(candies)):
        kept[candies[i]] -= 1
        if kept[candies[i]] == 0:
            distinct -= 1
        kept[candies[i - k]] += 1
        if kept[candies[i - k]] == 1:
            distinct += 1
        best = max(best, distinct)
    return best


seed = 2107


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        ([1, 2, 2, 3, 4, 3], 3),
        ([2, 2, 2, 2, 3, 3], 2),
        ([2, 4, 5], 0),
        ([1, 2, 3], 3),
        ([7, 7, 7, 7], 2),
        ([1, 2, 3, 4, 5], 1),
        ([1, 2, 9, 9, 1, 2], 2),
    ]
    for candies, k in examples:
        print(f"{show(candies)} sharing {k} -> {share_candies(candies, k)}")
    seed = 2107
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        flavors = next_random() % 8 + 1
        candies = [next_random() % flavors + 1 for _ in range(n)]
        k = next_random() % (n + 1)
        got = share_candies(candies, k)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 rows: {total} flavors kept, checksum {check}")
    cycled = [i % 1000 + 1 for i in range(100000)]
    distinct = list(range(1, 100001))
    print(f"cycled -> {share_candies(cycled, 50000)}")
    print(f"distinct, all but one -> {share_candies(distinct, 99999)}")
    print(f"distinct, 777 -> {share_candies(distinct, 777)}")


main()
