# LeetCode #1774: Closest Dessert Cost -- a Python mirror of the ★ arm: for
# each base, a depth-first search adding each topping none, once or twice,
# that stops adding once the cost has reached the target.


def better(cost, best, target):
    d, e = abs(cost - target), abs(best - target)
    return d < e or (d == e and cost < best)


def closest_cost(base_costs, topping_costs, target):
    best = base_costs[0]

    def add_toppings(i, cost):
        nonlocal best
        if better(cost, best, target):
            best = cost
        if i == len(topping_costs) or cost >= target:
            return
        for times in range(3):
            add_toppings(i + 1, cost + times * topping_costs[i])

    for base in base_costs:
        add_toppings(0, base)
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n costs from 1 to `most`
def random_costs(n, most):
    return [1 + next_random() % most for _ in range(n)]


def main():
    global seed
    # LeetCode's three examples
    print(f"{closest_cost([1, 7], [3, 4], 10)} {closest_cost([2, 3], [4, 5, 100], 18)} {closest_cost([3, 10], [2, 5], 9)}")
    # the edges
    print(f"{closest_cost([10], [1], 1)} {closest_cost([5], [1], 8)} {closest_cost([4], [2], 5)} {closest_cost([1, 2], [3], 10000)} {closest_cost([9, 4], [1, 2], 9)}")
    # the constraints' most
    seed = 1774
    bases = random_costs(10, 10000)
    toppings = random_costs(10, 10000)
    ones = [1] * 10
    print(f"the most: {closest_cost(bases, toppings, 10000)} {closest_cost(bases, toppings, 1)} {closest_cost(bases, ones, 10000)}")
    # 3000 random cases
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 10
        m = 1 + next_random() % 6
        most = 10 + next_random() % 9991
        bases = random_costs(n, most)
        toppings = random_costs(m, most)
        target = min(1 + next_random() % (2 * most), 10000)
        check = (check * 31 + closest_cost(bases, toppings, target)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
