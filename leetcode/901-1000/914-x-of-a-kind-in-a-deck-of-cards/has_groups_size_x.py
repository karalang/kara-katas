# LeetCode #914: X of a Kind in a Deck of Cards -- Python mirror of the
# counts' greatest common divisor in has_groups_size_x.kara, with the same
# test harness.


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def has_groups_size_x(deck):
    count = [0] * (max(deck) + 1)
    for card in deck:
        count[card] += 1
    g = 0
    for c in count:
        g = gcd(g, c)
    return g >= 2


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(deck):
    s = ",".join(str(v) for v in deck)
    print(f"deck = [{s}]: {'true' if has_groups_size_x(deck) else 'false'}")


def random_deck(kinds, rng, x, most, spoil):
    deck = []
    for _ in range(kinds):
        v = next_random() % rng
        copies = x * (1 + next_random() % most)
        for _ in range(copies):
            deck.append(v)
    if spoil and len(deck) > 1:
        deck.pop()
    i = len(deck)
    while i > 1:
        j = next_random() % i
        i -= 1
        deck[i], deck[j] = deck[j], deck[i]
    return deck


def show_size(deck):
    print(f"{len(deck)} cards: {'true' if has_groups_size_x(deck) else 'false'}")


def main():
    global seed
    show([1, 2, 3, 4, 4, 3, 2, 1])
    show([1, 1, 1, 2, 2, 2, 3, 3])
    show([1])
    show([1, 1])
    show([0, 0, 0, 1, 1, 1, 1, 1, 1])
    show([9999, 9999, 9999, 9999, 0, 0, 0, 0, 0, 0])
    show([5, 5, 5, 5, 5, 7, 7, 7])
    seed = 914
    yes = 0
    check = 0
    for c in range(600):
        x = 2 + next_random() % 12
        kinds = 1 + next_random() % 40
        rng = 3 if c % 3 == 0 else 100 if c % 3 == 1 else 10000
        most = 1 + next_random() % min(10000 // (x * kinds) + 1, 20)
        deck = random_deck(kinds, rng, x, most, c % 2 == 1)
        if len(deck) <= 10000:
            r = has_groups_size_x(deck)
            if r:
                yes += 1
            check = (check * 3 + (1 if r else 0)) % 1000000007
    print(f"600 decks: {yes} partitioned, checksum {check}")
    show_size([i % 5000 for i in range(10000)])
    show_size([i % 97 for i in range(9991)])
    show_size([1 if i == 0 else 0 for i in range(9999)])


main()
