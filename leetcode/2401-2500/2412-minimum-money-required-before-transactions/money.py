# LeetCode #2412: Minimum Money Required Before Transactions -- the mirror
# of the ★ arm: the total loss, and the largest of the losing transactions'
# cashbacks and the gaining ones' costs.

seed = 2412


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_money(transactions):
    loss = 0
    extra = 0
    for cost, cashback in transactions:
        if cost > cashback:
            loss += cost - cashback
            extra = max(extra, cashback)
        else:
            extra = max(extra, cost)
    return loss + extra


def transactions(n, top):
    out = []
    for _ in range(n):
        cost = (next_random() * 32768 + next_random()) % (top + 1)
        out.append((cost, (next_random() * 32768 + next_random()) % (top + 1)))
    return out


def main():
    print(minimum_money([(2, 1), (5, 0), (4, 2)]))
    print(minimum_money([(3, 0), (0, 3)]))
    print(minimum_money([(0, 0)]))
    print(minimum_money([(7, 2), (1, 9)]))
    print(minimum_money([(1, 5), (8, 8), (3, 4)]))
    print(minimum_money(transactions(100000, 1000000000)))
    print(minimum_money(transactions(100000, 10)))
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        a = minimum_money(transactions(n, 20))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
