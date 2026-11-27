# LeetCode #1833: Maximum Ice Cream Bars -- the ★ arm in Python


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


print(max_ice_cream([1, 3, 2, 4, 1], 7), max_ice_cream([10, 6, 8, 7, 7, 8], 5), max_ice_cream([1, 6, 3, 1, 2, 5], 20))
print(max_ice_cream([5], 5), max_ice_cream([6], 5), max_ice_cream([3, 3, 3, 3], 10), max_ice_cream([2, 9, 4], 16), max_ice_cream([100000], 100000000))
costs = []
for _ in range(100000):
    hi = next_random()
    costs.append(1 + (hi * 32768 + next_random()) % 100000)
print(f"the most: {max_ice_cream(costs, 100000000)} {max_ice_cream(costs, 1000)}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 10
    cs = [1 + next_random() % 20 for _ in range(n)]
    coins = 1 + next_random() % 60
    check = (check * 31 + max_ice_cream(cs, coins)) % 1000000007
print(f"3000 random cases: checksum {check}")
