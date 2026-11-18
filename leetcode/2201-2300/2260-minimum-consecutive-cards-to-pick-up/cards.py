# LeetCode #2260: Minimum Consecutive Cards to Pick Up -- Python mirror of
# the ★ arm (cards.kara): a dict from each value to where it was last
# seen, every repeat a candidate run. Output is byte-identical to the
# Kara arms.


def minimum_card_pickup(cards):
    last = {}
    best = -1
    for i, card in enumerate(cards):
        if card in last:
            run = i - last[card] + 1
            if best < 0 or run < best:
                best = run
        last[card] = i
    return best


# ---- test harness ---------------------------------------------------------

seed = 2260


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(length, values):
    return [next_random() % values for _ in range(length)]


def main():
    examples = [[3, 4, 2, 3, 4, 7], [1, 0, 5, 3], [1000000], [7, 7], [5, 1, 2, 3, 5], [9, 1, 2, 9, 4, 4]]
    for cards in examples:
        print(f"{cards} -> {minimum_card_pickup(cards)}")
    check = 0
    none = 0
    for t in range(5000):
        length = next_random() % 30 + 1
        answer = minimum_card_pickup(draw(length, [5, 20, 100, 1000][t % 4]))
        if answer < 0:
            none += 1
        check = (check * 31 + answer + 2) % 1000000007
    print(f"5000 hands: {none} with no pair, checksum {check}")
    all_different = [i * 10 for i in range(100000)]
    random = draw(100000, 1000001)
    twice = [i * 7919 % 50000 for i in range(100000)]
    far = list(range(100000))
    far[99999] = 0
    answers = [minimum_card_pickup(c) for c in [all_different, random, twice, far]]
    print(f"10^5 cards: {answers}")


main()
