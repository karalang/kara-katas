# LeetCode 746 — Min Cost Climbing Stairs, bench: the ★ arm (two running
# totals) on a staircase of 1000 steps whose costs keep changing.
# Mirrors min_cost_climbing_stairs.kara.


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


seed = 746


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 300000
    n = 1000
    cost = [next_random() % 1000 for _ in range(n)]
    total = 0
    for _ in range(rounds):
        for _ in range(5):
            i = next_random() % n
            cost[i] = next_random() % 1000
        total += min_cost_climbing_stairs(cost)
    print(f"{rounds} rounds on 1000 steps: least costs sum to {total}")


main()
