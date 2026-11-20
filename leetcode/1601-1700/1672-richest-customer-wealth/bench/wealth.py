# LeetCode #1672: Richest Customer Wealth -- the bench's Python mirror: the
# ★ arm on 4000 grids of 50 customers by 50 banks, up to 100 in each
# account, all drawn first, each answered 100 times.


def maximum_wealth(accounts):
    return max(sum(row) for row in accounts)


# ---- the harness ----------------------------------------------------------

seed = 1672


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


grids = 4000
side = 50
rounds = 100
all_grids = [[[next_random() % 100 + 1 for _ in range(side)] for _ in range(side)] for _ in range(grids)]
total = 0
check = 0
for r in range(rounds):
    for accounts in all_grids:
        richest = maximum_wealth(accounts)
        total += richest
        check = (check * 31 + richest + r) % 1000000007
print(f"{grids} grids of {side} by {side}, {rounds} rounds: answers sum to {total}, checksum {check}")
