# LeetCode #2706: Buy Two Chocolates -- the Python mirror of the star arm
# (chocolates.kara): one pass keeping the two cheapest prices; their sum
# is spent if the money covers it, and otherwise nothing is.


def buy_choco(prices, money):
    first = 101
    second = 101
    for p in prices:
        if p < first:
            second = first
            first = p
        elif p < second:
            second = p
    cost = first + second
    return money - cost if cost <= money else money


seed = 2706


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


print(buy_choco([1, 2, 2], 3))
print(buy_choco([3, 2, 3], 3))
print(buy_choco([1, 1], 2))
print(buy_choco([100, 100], 100))
print(buy_choco([100] * 49 + [1], 100))
print(buy_choco([50 - i for i in range(50)], 100))
total = 0
check = 0
for _ in range(5000):
    n = next_random() % 49 + 2
    prices = [next_random() % 100 + 1 for _ in range(n)]
    money = next_random() % 100 + 1
    left = buy_choco(prices, money)
    total += left
    check = (check * 31 + left) % 1000000007
print(f"5000 cases: money left sums to {total}, checksum {check}")
total = 0
check = 0
for _ in range(5000):
    n = next_random() % 4 + 2
    prices = [next_random() % 10 + 1 for _ in range(n)]
    money = next_random() % 20 + 1
    left = buy_choco(prices, money)
    total += left
    check = (check * 31 + left) % 1000000007
print(f"5000 cases of 2 to 5 prices up to 10: money left sums to {total}, checksum {check}")
