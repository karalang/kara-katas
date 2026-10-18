# LeetCode #714: Best Time to Buy and Sell Stock with Transaction Fee
# -- two running states. Benchmark mirror of the Kara star arm: the
# best cash holding no share and the best holding one, day by day.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


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


def main():
    seed = [714]
    walks = []
    for w in range(1, 11):
        step = 10 * w
        price = 50000
        prices = []
        for _ in range(100000):
            price += next_random(seed) % (2 * step + 1) - step
            if price < 1:
                price = 1
            prices.append(price)
        walks.append(prices)
    total = 0
    for rnd in range(300):
        fee = 3 * rnd
        for prices in walks:
            total += max_profit(prices, fee)
    print(f"300 rounds of 10 walks of 100000 days: sum {total}")


main()
