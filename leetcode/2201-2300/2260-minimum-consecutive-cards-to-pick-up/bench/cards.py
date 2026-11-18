# LeetCode #2260: Minimum Consecutive Cards to Pick Up -- Python mirror of
# the ★ arm (cards.kara) on the bench workload: a dict of where each value
# was last seen, every repeat a candidate run. Output is byte-identical to
# cards.kara.


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


# ---- bench harness ---------------------------------------------------------

seed = 2260


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    tops = [1000000, 100000, 10000]
    for t in range(300):
        cards = []
        for _ in range(100000):
            hi = next_random()
            cards.append((hi * 32768 + next_random()) % tops[t % 3])
        check = (check * 31 + minimum_card_pickup(cards) + 2) % 1000000007
    print(f"300 hands of 10^5 cards: checksum {check}")


main()
