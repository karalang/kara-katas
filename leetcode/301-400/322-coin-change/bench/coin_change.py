# Benchmark mirror of LeetCode #322 — same bottom-up table as
# bench/coin_change.kara.

AMOUNT = 1000000
COINS = 20
TOP = 3000
PASSES = 24
STRIDE = 9973
MODULUS = 1073741789


class Lcg:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def draw(self, bound):
        hi = self.next()
        lo = self.next()
        return (hi * 32768 + lo) % bound


def fewest(coins, amount, best):
    unreachable = amount + 1
    best[0] = 0
    for a in range(1, amount + 1):
        b = unreachable
        for c in coins:
            if c <= a and best[a - c] + 1 < b:
                b = best[a - c] + 1
        best[a] = b
    if best[amount] == unreachable:
        return -1
    return best[amount]


def main():
    rng = Lcg(322)
    sink = 0
    reached = 0
    best = [0] * (AMOUNT + 1)
    for p in range(PASSES):
        g = 1 + p % 3
        coins = []
        while len(coins) < COINS:
            c = g * (rng.draw(TOP // g) + 1)
            if c not in coins:
                coins.append(c)
        amount = AMOUNT // 2 + rng.draw(AMOUNT // 2 + 1)
        ans = fewest(coins, amount, best)
        if ans >= 0:
            reached += 1
        probe = 0
        a = 0
        while a <= amount:
            probe = (probe * 31 + best[a]) % MODULUS
            a += STRIDE
        sink = (sink * 131 + ans + 1 + probe) % MODULUS
    print(f"sink {sink} reached {reached}")


main()
