# LeetCode #2347: Best Poker Hand -- the bench, the ★ arm in Python: a
# flush when every suit equals the first; otherwise the most cards of one
# rank, counted in a table of 14, names the hand.


def best_hand(ranks, suits):
    flush = True
    for s in suits:
        if s != suits[0]:
            flush = False
    if flush:
        return "Flush"
    count = [0] * 14
    most = 0
    for r in ranks:
        count[r] += 1
        most = max(most, count[r])
    if most >= 3:
        return "Three of a Kind"
    elif most == 2:
        return "Pair"
    else:
        return "High Card"


SEED = [2347]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # five different cards of 52, any card already in the hand drawn again
    hands = []
    for _ in range(100000):
        cards = []
        while len(cards) < 5:
            card = next_random() % 52
            if card not in cards:
                cards.append(card)
        hands.append(([c % 13 + 1 for c in cards], [chr(97 + c // 13) for c in cards]))
    check = 0
    for p in range(30):
        for ranks, suits in hands:
            check = (check * 31 + len(best_hand(ranks, suits)) + p) % 1000000007
    print(f"30 passes over 10^5 hands: checksum {check}")


main()
