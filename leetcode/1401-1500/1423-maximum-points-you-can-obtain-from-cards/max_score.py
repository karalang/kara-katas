# LeetCode #1423, Python mirror of max_score.kara: the first k cards
# taken, then one at a time the last of those given back for the next
# card from the far end, the best total kept.


def max_score(card_points, k):
    n = len(card_points)
    total = sum(card_points[:k])
    best = total
    for i in range(k):
        total += card_points[n - 1 - i] - card_points[k - 1 - i]
        best = max(best, total)
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, top):
    return [1 + next_random() % top for _ in range(n)]


def main():
    global seed
    firsts = [
        max_score([1, 2, 3, 4, 5, 6, 1], 3),
        max_score([2, 2, 2], 2),
        max_score([9, 7, 7, 9, 7, 7, 9], 7),
        max_score([1, 1000, 1], 1),
        max_score([1, 79, 80, 1, 1, 1, 200, 1], 3),
        max_score([100, 40, 17, 9, 73, 75], 3),
    ]
    print(" ".join(str(x) for x in firsts))
    seed = 1423
    most = [10000] * 100000
    cards = drawn(100000, 10000)
    print(f"10^5 cards: {max_score(most, 100000)} {max_score(cards, 1)} {max_score(cards, 50000)} {max_score(cards, 99999)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        top = [10, 100, 10000][next_random() % 3]
        k = 1 + next_random() % n
        got = max_score(drawn(n, top), k)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
