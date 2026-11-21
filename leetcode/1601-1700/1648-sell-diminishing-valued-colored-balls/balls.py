# LeetCode #1648: Sell Diminishing-Valued Colored Balls -- the Python mirror
# of the ★ arm: the counts sorted largest first and sold from the top down
# in layers, each layer whole rows of an arithmetic series.

MOD = 1_000_000_007


def max_profit(inventory, orders):
    counts = sorted(inventory, reverse=True) + [0]
    profit = 0
    for i in range(len(counts) - 1):
        width = i + 1
        high, low = counts[i], counts[i + 1]
        if high == low:
            continue

        def series(stop):
            return (high + stop + 1) * (high - stop) // 2 % MOD * width % MOD

        if width * (high - low) < orders:
            profit = (profit + series(low)) % MOD
            orders -= width * (high - low)
        else:
            rows = orders // width
            rest = orders % width
            profit = (profit + series(high - rows)) % MOD
            profit = (profit + rest * (high - rows) % MOD) % MOD
            return profit
    return profit


# ---- the harness: the same as every arm's ---------------------------------

seed = 1648


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        inventory = []
        balls = 0
        for _ in range(n):
            b = (next_random() * 32768 + next_random()) % top + 1
            inventory.append(b)
            balls += b
        orders = (next_random() * 32768 + next_random()) % min(balls, 1000000000) + 1
        profit = max_profit(inventory, orders)
        total += profit
        check = (check * 31 + profit + 1) % 1000000007
    print(f"{count} inventories of up to {most} colors: profits sum to {total}, checksum {check}")


print(max_profit([2, 5], 4))
print(max_profit([3, 5], 6))
print(max_profit([7], 7))
print(max_profit([4, 4, 4], 5))
print(max_profit([1000000000], 1000000000))
batch(3000, 4, 6)
batch(1000, 100, 1000000000)
batch(20, 100000, 1000000000)
