# Benchmark for #638: mirror of shopping_offers.kara (the ★ arm: search
# over what is still needed, with a memo keyed by the needs) on the same
# workload. The needs are a tuple, so they can key the dict.

ROUNDS = 800


def cheapest(price, special, needs, memo):
    known = memo.get(needs)
    if known is not None:
        return known
    n = len(needs)
    best = 0
    for i in range(n):
        best += needs[i] * price[i]
    for offer in special:
        rest = []
        fits = True
        any_item = False
        for i in range(n):
            if offer[i] > needs[i]:
                fits = False
            if offer[i] > 0:
                any_item = True
            rest.append(needs[i] - offer[i])
        if fits and any_item:
            cost = offer[n] + cheapest(price, special, tuple(rest), memo)
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


def main():
    prices = []
    needs = []
    offers = []
    for _ in range(20):
        price = []
        need = []
        for _ in range(6):
            price.append(1 + next_random() % 10)
            need.append(next_random() % 5)
        special = []
        for _ in range(100):
            offer = [next_random() % 3 for _ in range(6)]
            offer.append(next_random() % 51)
            special.append(offer)
        prices.append(price)
        needs.append(need)
        offers.append(special)
    total = 0
    checksum = 0
    for r in range(ROUNDS):
        s = r % 20
        paid = shopping_offers(prices[s], offers[s], needs[s])
        total += paid
        checksum = (checksum * 31 + paid) % 1000000007
    print(f"20 shops, {ROUNDS} rounds: total {total}, checksum {checksum}")


main()
