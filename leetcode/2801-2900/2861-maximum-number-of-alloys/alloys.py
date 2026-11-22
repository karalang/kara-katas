# LeetCode #2861: Maximum Number of Alloys -- the ★ arm's mirror: a
# binary search per machine on the count, the cost of x alloys every
# metal's shortfall bought at its price; the best machine wins.


def max_number_of_alloys(n, k, budget, composition, stock, cost):
    best = 0
    for machine in composition:
        def price(x):
            return sum(max(machine[j] * x - stock[j], 0) * cost[j] for j in range(n))
        lo, hi = 0, 200000000
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if price(mid) <= budget:
                lo = mid
            else:
                hi = mid - 1
        best = max(best, lo)
    return best


seed = 2861


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def grid(rows, cols, low, top):
    return [[low + wide() % (top - low + 1) for _ in range(cols)] for _ in range(rows)]


def main():
    comp = [[1, 1, 1], [1, 1, 10]]
    a = max_number_of_alloys(3, 2, 15, comp, [0, 0, 0], [1, 2, 3])
    b = max_number_of_alloys(3, 2, 15, comp, [0, 0, 100], [1, 2, 3])
    c = max_number_of_alloys(2, 3, 10, [[2, 1], [1, 2], [1, 1]], [1, 1], [5, 5])
    most = max_number_of_alloys(100, 100, 100000000, [[1] * 100 for _ in range(100)], [100000000] * 100, [1] * 100)
    print(f"{a} {b} {c} {most}")
    total = check = 0
    for c in range(3030):
        small = c < 3000
        if small:
            n = next_random() % 4 + 1
            k = next_random() % 3 + 1
            mc, ms, mo, mb = 5, 20, 5, 50
        else:
            n = next_random() % 100 + 1
            k = next_random() % 100 + 1
            mc, ms, mo, mb = 100, 100000000, 100, 100000000
        composition = grid(k, n, 1, mc)
        stock = grid(1, n, 0, ms)[0]
        cost = grid(1, n, 1, mo)[0]
        budget = wide() % (mb + 1)
        alloys = max_number_of_alloys(n, k, budget, composition, stock, cost)
        total += alloys
        check = (check * 31 + alloys) % 1000000007
        if c == 2999:
            print(f"3000 small cases: {total} alloys, checksum {check}")
            total = check = 0
    print(f"30 large cases: {total} alloys, checksum {check}")


main()
