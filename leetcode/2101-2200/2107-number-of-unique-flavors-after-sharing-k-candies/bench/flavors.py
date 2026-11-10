# LeetCode #2107: Number of Unique Flavors After Sharing K Candies -- the
# benchmark, the same algorithm as flavors.kara: a dict of the kept
# flavors' counts, the shared window sliding right one candy at a time.


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


def main():
    rows = []
    for _ in range(20):
        flavors = next_random() % 5000 + 1
        rows.append([next_random() % flavors + 1 for _ in range(100000)])
    total = 0
    check = 0
    for candies in rows:
        for _ in range(5):
            hi = next_random()
            k = (hi * 32768 + next_random()) % 100001
            got = share_candies(candies, k)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"100 shares: {total} flavors kept, checksum {check}")


main()
