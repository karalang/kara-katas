# LeetCode #714: Best Time to Buy and Sell Stock with Transaction Fee
# -- two running states.
#
# A mirror of best_time_to_buy_and_sell_stock_with_transaction_fee.kara
# (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_profit(prices, fee):
    cash = 0
    hold = -prices[0]
    for i in range(1, len(prices)):
        sold = hold + prices[i] - fee
        if sold > cash:
            cash = sold
        bought = cash - prices[i]
        if bought > hold:
            hold = bought
    return cash


def show(prices, fee):
    shown = "[" + ", ".join(str(x) for x in prices) + "]"
    print(f"{shown}, fee {fee} -> {max_profit(prices, fee)}")


def main():
    global seed
    show([1, 3, 2, 8, 4, 9], 2)
    show([1, 3, 7, 5, 10, 3], 3)
    show([5], 0)
    show([5, 4, 3, 2, 1], 0)
    show([1, 2, 3, 4, 5], 0)
    show([1, 2, 3, 4, 5], 4)
    show([1, 2, 3, 4, 5], 3)
    show([1, 5, 1, 5, 1, 5], 0)
    show([1, 5, 1, 5, 1, 5], 3)
    show([1, 5, 1, 5, 1, 5], 4)
    show([2, 1, 4, 4, 2, 3, 2, 5, 1, 2], 1)
    seed = 714
    walk = []
    price = 25000
    for _ in range(50000):
        price += next_random() % 201 - 100
        price = max(1, min(49999, price))
        walk.append(price)
    print(f"50000-day walk, fee 0: {max_profit(walk, 0)}")
    print(f"50000-day walk, fee 50: {max_profit(walk, 50)}")
    print(f"50000-day walk, fee 49999: {max_profit(walk, 49999)}")
    noise = [1 + next_random() % 49999 for _ in range(50000)]
    print(f"50000 random prices, fee 1000: {max_profit(noise, 1000)}")
    total = 0
    for _ in range(500):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 50
        prices = [1 + next_random() % top for _ in range(n)]
        fee = next_random() % 20
        total = (total * 131 + max_profit(prices, fee)) % 1000000007
    print(f"500 random price lists: checksum {total}")


main()
