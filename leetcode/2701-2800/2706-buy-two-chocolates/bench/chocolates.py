# LeetCode #2706: Buy Two Chocolates -- the bench (chocolates.kara in
# Python): one pass keeping the two cheapest prices.


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


lists, rounds = 100000, 10
problems = []
for _ in range(lists):
    prices = [next_random() % 100 + 1 for _ in range(50)]
    money = next_random() % 100 + 1
    problems.append((prices, money))
total = 0
check = 0
for r in range(rounds):
    for prices, money in problems:
        left = buy_choco(prices, money)
        total += left
        check = (check * 31 + left + r) % 1000000007
print(f"{lists} lists of 50 prices, {rounds} rounds: money left sums to {total}, checksum {check}")
