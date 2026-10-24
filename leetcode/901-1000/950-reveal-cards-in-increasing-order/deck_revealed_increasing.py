# LeetCode #950: Reveal Cards In Increasing Order -- the reveals played on
# the places. Mirrors deck_revealed_increasing.kara (the ★ arm) and its
# harness.
from collections import deque


def deck_revealed_increasing(deck):
    places = deque(range(len(deck)))
    out = [0] * len(deck)
    for card in sorted(deck):
        out[places.popleft()] = card
        if places:
            places.append(places.popleft())
    return out


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


seed = 950


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_deck(n, top):
    taken = set()
    deck = []
    while len(deck) < n:
        a = next_random()
        b = next_random()
        v = 1 + (a * 32768 + b) % top
        if v not in taken:
            taken.add(v)
            deck.append(v)
    return deck


def fold(check, v):
    for x in v:
        check = (check * 1000003 + x) % 1000000007
    return check


def main():
    examples = [
        [17, 13, 11, 2, 3, 5, 7],
        [1, 1000],
        [5],
        [2, 1],
        [1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [1000000, 1, 500000],
    ]
    for deck in examples:
        print(f"{show(deck)} -> {show(deck_revealed_increasing(deck))}")
    cards = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        deck = random_deck(n, 100)
        cards += n
        check = fold(check, deck_revealed_increasing(deck))
    print(f"300 random decks of {cards} cards: checksum {check}")
    big = [random_deck(1000, 1000000)]
    big.append([i + 1 for i in range(1000)])
    big.append([1000000 - i for i in range(1000)])
    big.append([(i * 7919) % 1000 * 1000 + 1 for i in range(1000)])
    for deck in big:
        out = deck_revealed_increasing(deck)
        print(f"1000 cards, first {show(out[:8])}, last {out[999]}, checksum {fold(0, out)}")


main()
