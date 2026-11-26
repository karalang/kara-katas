def max_score(card_points, k):
    n = len(card_points)
    total = sum(card_points[:k])
    best = total
    for i in range(k):
        total += card_points[n - 1 - i] - card_points[k - 1 - i]
        best = max(best, total)
    return best


def main():
    seed = 1423
    pool = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(1 + seed // 65536 % 10000)
    check = 0
    for _ in range(50000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 900001
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + seed // 65536 % 100000
        check = (check * 131 + max_score(pool[start:start + 100000], k)) % 1000000007
    print(f"5 * 10^4 windows of 10^5 cards: checksum {check}")


main()
