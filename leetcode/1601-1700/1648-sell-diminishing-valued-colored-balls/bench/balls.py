# LeetCode #1648: Sell Diminishing-Valued Colored Balls -- the bench's
# Python mirror: the ★ arm on 100 random inventories of 100000 colors with
# up to 10^9 balls each, and an order for up to 10^9 of them, all drawn
# first.

MOD = 1_000_000_007


def max_profit(inventory, orders):
    counts = sorted(inventory, reverse=True) + [0]
    profit = 0
    for i in range(len(counts) - 1):
        width = i + 1
        high, low = counts[i], counts[i + 1]
        if high == low:
            continue
        if width * (high - low) < orders:
            profit = (profit + (high + low + 1) * (high - low) // 2 % MOD * width % MOD) % MOD
            orders -= width * (high - low)
        else:
            rows = orders // width
            rest = orders % width
            stop = high - rows
            profit = (profit + (high + stop + 1) * (high - stop) // 2 % MOD * width % MOD) % MOD
            profit = (profit + rest * stop % MOD) % MOD
            return profit
    return profit


seed = 1648


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


cases = []
for _ in range(100):
    inventory = [(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(100000)]
    orders = (next_random() * 32768 + next_random()) % 1000000000 + 1
    cases.append((inventory, orders))
check = 0
total = 0
for inventory, orders in cases:
    profit = max_profit(inventory, orders)
    total += profit
    check = (check * 31 + profit + 1) % 1000000007
print(f"100 inventories of 100000 colors: profits sum to {total}, checksum {check}")
