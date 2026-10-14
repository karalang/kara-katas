# LeetCode #638: Shopping Offers -- Python mirror of the ★ arm.
#
# Depth-first search over what is still needed, remembering the cheapest
# price of every need seen.


def cheapest(price, special, needs, memo):
    if needs in memo:
        return memo[needs]
    n = len(needs)
    best = 0
    for i in range(n):
        best += needs[i] * price[i]
    for offer in special:
        fits = all(offer[i] <= needs[i] for i in range(n))
        if fits and any(offer[i] > 0 for i in range(n)):
            rest = tuple(needs[i] - offer[i] for i in range(n))
            cost = offer[n] + cheapest(price, special, rest, memo)
            if cost < best:
                best = cost
    memo[needs] = best
    return best


def shopping_offers(price, special, needs):
    return cheapest(price, special, tuple(needs), {})


seed = 638


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_offers(n, count, most):
    special = []
    for _ in range(count):
        offer = [next_random() % (most + 1) for _ in range(n)]
        offer.append(next_random() % 51)
        special.append(offer)
    return special


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def ask(price, special, needs):
    offers = "[" + ", ".join(show(o) for o in special) + "]"
    print(f"price {show(price)}, offers {offers}, needs {show(needs)} -> "
          f"{shopping_offers(price, special, needs)}")


def main():
    ask([2, 5], [[3, 0, 5], [1, 2, 10]], [3, 2])
    ask([2, 3, 4], [[1, 1, 0, 4], [2, 2, 1, 9]], [1, 2, 1])
    ask([3, 4], [], [2, 1])
    ask([3, 4], [[1, 1, 1]], [0, 0])
    ask([1, 1], [[1, 1, 3]], [2, 2])
    ask([5], [[0, 0]], [3])
    ask([5, 5], [[2, 0, 1], [0, 4, 1]], [1, 3])
    ask([10], [[2, 1]], [10])
    ask([4, 4, 4], [[1, 1, 0, 7], [0, 1, 1, 7], [1, 0, 1, 7]], [2, 2, 2])
    ask([0, 7], [[3, 1, 6]], [3, 1])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 6
        price = []
        needs = []
        for _ in range(n):
            price.append(next_random() % 11)
            needs.append(next_random() % 4)
        count = next_random() % 13
        special = random_offers(n, count, 2)
        paid = shopping_offers(price, special, needs)
        total += paid
        checksum = (checksum * 31 + paid) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    price = [10, 9, 8, 7, 6, 5]
    needs = [10, 9, 8, 3, 2, 1]
    special = random_offers(6, 100, 3)
    full = 10 * 10 + 9 * 9 + 8 * 8 + 7 * 3 + 6 * 2 + 5
    print(f"6 items, 100 offers, needs {show(needs)}: "
          f"{shopping_offers(price, special, needs)} (list price {full})")


main()
