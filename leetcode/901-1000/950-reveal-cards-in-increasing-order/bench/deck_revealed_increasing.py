# Benchmark: LeetCode #950 Reveal Cards In Increasing Order -- the ★ arm,
# the reveals played on the places, on decks of 1000 cards, LeetCode's
# largest. Mirrors deck_revealed_increasing.kara, .c, .rs and go-seq/.
from collections import deque


def deck_revealed_increasing(deck):
    places = deque(range(len(deck)))
    out = [0] * len(deck)
    for card in sorted(deck):
        out[places.popleft()] = card
        if places:
            places.append(places.popleft())
    return out


seed = 950


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 1000, 20, 1000
    decks = []
    for _ in range(count):
        taken = set()
        deck = []
        while len(deck) < n:
            a = next_random()
            b = next_random()
            v = 1 + (a * 32768 + b) % 1000000
            if v not in taken:
                taken.add(v)
                deck.append(v)
        decks.append(deck)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            out = deck_revealed_increasing(decks[(r + i) % count])
            total += out[n - 1]
            check = (check * 1000003 + out[(r * 7 + i) % n]) % 1000000007
    print(f"{rounds} rounds over {count} decks of {n} cards: last cards adding to {total}, checksum {check}")


main()
