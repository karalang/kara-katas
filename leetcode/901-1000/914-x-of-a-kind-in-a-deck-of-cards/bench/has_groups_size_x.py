# LeetCode #914: X of a Kind in a Deck of Cards -- bench: Python mirror of
# the counts' greatest common divisor in has_groups_size_x.kara.


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def has_groups_size_x(deck):
    largest = 0
    for card in deck:
        largest = max(largest, card)
    count = [0] * (largest + 1)
    for card in deck:
        count[card] += 1
    g = 0
    for c in count:
        g = gcd(g, c)
    return g >= 2


seed = 914


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 20000
    deck = []
    for v in range(1666):
        for _ in range(6):
            deck.append(v * 6)
    n = len(deck)
    yes = 0
    check = 0
    for r in range(rounds):
        high = next_random()
        i = (high * 32768 + next_random()) % n
        old = deck[i]
        deck[i] = old + next_random() % 3 * 6
        if deck[i] > 9995:
            deck[i] = old
        if has_groups_size_x(deck):
            yes += 1
            check = (check * 31 + r) % 1000000007
        deck[i] = old
    print(f"{rounds} rounds over {n} cards: {yes} partitioned, checksum {check}")


main()
