# LeetCode #2312: Selling Pieces of Wood -- the bench, the ★ arm in
# Python. Bottom up over every size: each piece its own price or the
# most of any one cut across it.

seed = 2312


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


lists = []
for _ in range(10):
    used = [False] * (200 * 200)
    prices = []
    for _ in range(2000):
        h = next_random() % 200 + 1
        w = next_random() % 200 + 1
        price = next_random() % 1000000 + 1
        if not used[(h - 1) * 200 + w - 1]:
            used[(h - 1) * 200 + w - 1] = True
            prices.append((h, w, price))
    lists.append(prices)
check = 0
for p in range(2):
    for a in range(10):
        prices = [(h, w, price + p) for h, w, price in lists[a]]
        check = (check * 31 + selling_wood(200, 200, prices)) % 1000000007
print(f"2 passes over 10 lists of 2000 prices on 200 by 200: checksum {check}")
