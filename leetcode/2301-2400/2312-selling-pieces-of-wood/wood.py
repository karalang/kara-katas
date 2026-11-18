# LeetCode #2312: Selling Pieces of Wood -- the ★ arm in Python. Bottom
# up over every size: best[h][w] is the most an h by w piece fetches,
# its own price if it has one, or the most of any one cut across it.


def selling_wood(m, n, prices):
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for h, w, price in prices:
        best[h][w] = price
    for h in range(1, m + 1):
        for w in range(1, n + 1):
            for i in range(1, h):
                best[h][w] = max(best[h][w], best[i][w] + best[h - i][w])
            for j in range(1, w):
                best[h][w] = max(best[h][w], best[h][j] + best[h][w - j])
    return best[m][n]


seed = 2312


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make(m, n, count, most):
    used = [False] * (m * n)
    prices = []
    for _ in range(count):
        h = next_random() % m + 1
        w = next_random() % n + 1
        price = next_random() % most + 1
        if not used[(h - 1) * n + w - 1]:
            used[(h - 1) * n + w - 1] = True
            prices.append((h, w, price))
    return prices


def main():
    print(selling_wood(3, 5, [(1, 4, 2), (2, 2, 7), (2, 1, 3)]))
    print(selling_wood(4, 6, [(3, 2, 10), (1, 4, 2), (4, 1, 3)]))
    print(selling_wood(2, 3, [(2, 3, 50), (1, 1, 1)]))
    print(selling_wood(2, 3, [(2, 2, 9)]))
    print(selling_wood(3, 3, [(1, 1, 5), (3, 3, 40), (1, 3, 14)]))
    print(selling_wood(100, 100, make(100, 100, 2000, 1000000)))
    check = 0
    total = 0
    for _ in range(300):
        m = next_random() % 12 + 1
        n = next_random() % 12 + 1
        count = next_random() % 20 + 1
        money = selling_wood(m, n, make(m, n, count, 100))
        check = (check * 31 + money) % 1000000007
        total += money
    print(f"300 pieces: checksum {check}, {total} in all")


main()
