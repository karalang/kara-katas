"""LeetCode #322: Coin Change — Python mirror of coin_change.kara.

Same algorithm (bottom-up DP over every amount, sentinel amount + 1 for
unreachable), same demo cases, byte-identical output."""


def coin_change(coins: list[int], amount: int) -> int:
    unreachable = amount + 1
    best = [unreachable] * (amount + 1)
    best[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    if best[amount] == unreachable:
        return -1
    return best[amount]


def show(v: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in v) + "]"


def report(coins: list[int], amount: int) -> None:
    print(f"{show(coins)} amount={amount} -> {coin_change(coins, amount)}")


class Lcg:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def next(self) -> int:
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def denominations(count: int, top: int, rng: Lcg) -> list[int]:
    v: list[int] = []
    while len(v) < count:
        c = rng.next() % top + 1
        if c not in v:
            v.append(c)
    return v


def main() -> None:
    report([1, 2, 5], 11)
    report([2], 3)
    report([1], 0)

    report([1, 3, 4], 6)
    report([1, 5, 6, 9], 11)
    report([186, 419, 83, 408], 6249)

    report([4, 6], 9)
    report([4, 6], 14)
    report([7, 11], 59)
    report([7, 11], 60)

    report([13], 13)
    report([50, 20], 10)
    report([9, 2, 7, 3], 23)
    report([5, 7], 0)

    rng = Lcg(322)
    for count in [2, 3, 4]:
        coins = denominations(count, 12, rng)
        amount = rng.next() % 40
        report(coins, amount)

    for t, amount in enumerate([1000, 20000, 100000]):
        coins = denominations(6 + t, 500 + 300 * t, rng)
        print(f"{show(coins)} amount={amount} -> {coin_change(coins, amount)}")


if __name__ == "__main__":
    main()
