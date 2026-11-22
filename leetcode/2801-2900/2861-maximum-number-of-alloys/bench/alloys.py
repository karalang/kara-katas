# LeetCode #2861: Maximum Number of Alloys -- the bench: the ★ arm over
# 100 cases of 100 metals and 100 machines, LeetCode's most, amounts
# drawn over LeetCode's full ranges, all drawn first, then each
# answered 20 times.


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


def main():
    count, rounds, n = 100, 20, 100
    seed = 2861

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    cases = []
    for _ in range(count):
        composition = [[1 + wide() % 100 for _ in range(n)] for _ in range(n)]
        stock = [wide() % 100000001 for _ in range(n)]
        cost = [1 + wide() % 100 for _ in range(n)]
        budget = wide() % 100000001
        cases.append((budget, composition, stock, cost))
    total = check = 0
    for r in range(rounds):
        for budget, composition, stock, cost in cases:
            alloys = max_number_of_alloys(n, n, budget, composition, stock, cost)
            total += alloys
            check = (check * 31 + alloys + r) % 1000000007
    print(f"{count} cases of {n} by {n}, {rounds} rounds: {total} alloys, checksum {check}")


main()
