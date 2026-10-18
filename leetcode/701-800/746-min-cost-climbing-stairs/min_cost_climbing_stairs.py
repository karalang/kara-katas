# LeetCode 746 — Min Cost Climbing Stairs, two running totals.
# Mirror of min_cost_climbing_stairs.kara (the ★ arm); same output, byte for byte.


def min_cost_climbing_stairs(cost):
    before = 0
    here = 0
    for i in range(2, len(cost) + 1):
        a = before + cost[i - 2]
        b = here + cost[i - 1]
        nxt = a if a < b else b
        before = here
        here = nxt
    return here


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(cost):
    print(f"[{', '.join(map(str, cost))}] -> {min_cost_climbing_stairs(cost)}")


def main():
    show([10, 15, 20])
    show([1, 100, 1, 1, 1, 100, 1, 1, 100, 1])
    show([0, 0])
    show([5, 3])
    show([0, 0, 0, 1])
    show([1, 0, 0, 1, 0, 0, 1])
    show([999, 999, 999, 999, 999])

    rng = Rng(746)
    big = [rng.next() % 1000 for _ in range(1000)]
    print(f"1000 random steps: {min_cost_climbing_stairs(big)}")
    print(f"1000 steps of 999: {min_cost_climbing_stairs([999] * 1000)}")

    total = 0
    check = 0
    for _ in range(300):
        n = 2 + rng.next() % 14
        cost = [rng.next() % 20 for _ in range(n)]
        got = min_cost_climbing_stairs(cost)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"300 random stairs: costs sum to {total}, checksum {check}")


main()
