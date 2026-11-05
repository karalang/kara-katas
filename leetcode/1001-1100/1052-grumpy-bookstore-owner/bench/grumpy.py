# LeetCode #1052: Grumpy Bookstore Owner -- Python mirror of
# bench/grumpy.kara.


def max_satisfied(customers, grumpy, minutes):
    base = 0
    saved = 0
    best = 0
    for i in range(len(customers)):
        if grumpy[i] == 0:
            base += customers[i]
        else:
            saved += customers[i]
        if i >= minutes and grumpy[i - minutes] == 1:
            saved -= customers[i - minutes]
        best = max(best, saved)
    return base + best


seed = 1052


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    days, n, techniques = 200, 20000, 10
    all_days = []
    for _ in range(days):
        customers = []
        grumpy = []
        for _ in range(n):
            customers.append(next_random() % 1001)
            grumpy.append(next_random() % 2)
        all_days.append((customers, grumpy))
    total = 0
    check = 0
    for customers, grumpy in all_days:
        for _ in range(techniques):
            minutes = next_random() % n + 1
            answer = max_satisfied(customers, grumpy, minutes)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{days} days of {n} minutes, {techniques} techniques each: total {total}, checksum {check}")


main()
