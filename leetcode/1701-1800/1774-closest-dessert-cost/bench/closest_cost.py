# LeetCode #1774: Closest Dessert Cost -- the bench in Python, mirroring
# closest_cost.kara: a depth-first search over the toppings for each base.
import sys

sys.setrecursionlimit(10000)


def better(cost, best, target):
    d, e = abs(cost - target), abs(best - target)
    return d < e or (d == e and cost < best)


def add_toppings(toppings, i, cost, target, best):
    if better(cost, best[0], target):
        best[0] = cost
    if i == len(toppings) or cost >= target:
        return
    for times in range(3):
        add_toppings(toppings, i + 1, cost + times * toppings[i], target, best)


def closest_cost(base_costs, topping_costs, target):
    best = [base_costs[0]]
    for base in base_costs:
        add_toppings(topping_costs, 0, base, target, best)
    return best[0]


seed = 1774


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_costs(n, most):
    return [1 + next_random() % most for _ in range(n)]


def main():
    bases = []
    toppings = []
    for _ in range(100):
        bases.append(random_costs(10, 5000))
        toppings.append(random_costs(8, 1000))
    check = 0
    for call in range(1000):
        target = 1 + (check + call * 7919) % 10000
        cost = closest_cost(bases[(check + call) % 100], toppings[(check // 100 + call * 31) % 100], target)
        check = (check * 31 + cost) % 1000000007
    print(f"1000 calls over 100 menus: checksum {check}")


main()
