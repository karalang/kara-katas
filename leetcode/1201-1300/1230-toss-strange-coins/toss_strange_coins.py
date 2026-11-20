# LeetCode #1230: Toss Strange Coins -- Python mirror of the ★ arm: one row
# of the table, the probability of each count of heads so far, updated from
# the top count down for each coin.


def probability_of_heads(prob, target):
    ways = [0.0] * (target + 1)
    ways[0] = 1.0
    for p in prob:
        for j in range(target, 0, -1):
            ways[j] = ways[j] * (1.0 - p) + ways[j - 1] * p
        ways[0] = ways[0] * (1.0 - p)
    return ways[target]


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def coin(seed):
    r = next_random(seed) % 120
    return 0.0 if r < 6 else 1.0 if r < 12 else (r - 12) / 108.0


def main():
    print(f"{probability_of_heads([0.4], 1):.5f}")
    print(f"{probability_of_heads([0.5, 0.5, 0.5, 0.5, 0.5], 0):.5f}")
    print(f"{probability_of_heads([1.0, 0.0, 1.0], 2):.5f}")
    print(f"{probability_of_heads([1.0, 0.0, 1.0], 1):.5f}")
    seed = [1230]
    total = 0.0
    impossible = 0
    for _ in range(500):
        n = next_random(seed) % 60 + 1
        prob = [coin(seed) for _ in range(n)]
        target = next_random(seed) % (n + 1)
        p = probability_of_heads(prob, target)
        total += p
        if p == 0.0:
            impossible += 1
    print(f"500 random sets: total {total:.6f}, {impossible} impossible")
    prob = [(i % 97) / 96.0 for i in range(1000)]
    fair = [0.5] * 1000
    print(f"1000 coins: {probability_of_heads(prob, 500):.5f}, {probability_of_heads(prob, 480):.5f}, {probability_of_heads(fair, 500):.5f}")


main()
