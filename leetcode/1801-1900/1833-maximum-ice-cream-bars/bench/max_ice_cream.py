# LeetCode #1833: Maximum Ice Cream Bars -- the bench in Python: the ★ arm
# over 1000 calls on the first 50000 to 99999 of one list of 10^5 bars of 1 to
# 10^5 coins, built once, with 10^6 to 10^8 coins, each run's length and coins
# drawn from the checksum so far. Each call copies its run, as the arm takes
# its list by value.


def max_ice_cream(costs, coins):
    dearest = max(costs)
    count = [0] * (dearest + 1)
    for c in costs:
        count[c] += 1
    left = coins
    bars = 0
    for price in range(1, dearest + 1):
        if price > left:
            break
        bought = min(count[price], left // price)
        bars += bought
        left -= bought * price
    return bars


seed = 1833


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


base = []
for _ in range(100000):
    hi = next_random()
    base.append(1 + (hi * 32768 + next_random()) % 100000)
check = 0
for call in range(1000):
    n = 50000 + (check + call) % 50000
    coins = 1000000 + (check * 7 + call) % 99000000
    check = (check * 31 + max_ice_cream(base[:n], coins)) % 1000000007
print(f"1000 calls: checksum {check}")
