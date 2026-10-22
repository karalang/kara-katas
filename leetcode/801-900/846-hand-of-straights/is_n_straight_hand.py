# LeetCode #846: Hand of Straights -- Python mirror of the ★ arm and its harness.
#
# Python has no sorted map, so the mirror keeps a dict of counts and a
# sorted list of its keys, reading the smallest key left from the front
# of that list: the same groups, dealt in the same order.


def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size != 0:
        return False
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    keys = sorted(counts)
    at = 0
    while at < len(keys):
        low = keys[at]
        if low not in counts:
            at += 1
            continue
        starts = counts[low]
        for card in range(low, low + group_size):
            have = counts.get(card, 0)
            if have < starts:
                return False
            if have == starts:
                del counts[card]
            else:
                counts[card] = have - starts
    return True


def show(hand, group_size):
    ok = "true" if is_n_straight_hand(hand, group_size) else "false"
    print(f"[{', '.join(map(str, hand))}], {group_size} -> {ok}")


seed = 846


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffle(cards):
    n = len(cards)
    for i in range(n):
        j = i + next_random() % (n - i)
        cards[i], cards[j] = cards[j], cards[i]


def b(x):
    return "true" if x else "false"


def main():
    for hand, g in [([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), ([1, 2, 3, 4, 5], 4), ([1], 1),
                    ([5, 1, 5], 1), ([3, 1, 2], 3), ([1, 2, 4], 3), ([2, 1], 2),
                    ([1, 1, 2, 2, 3, 3], 3), ([1, 1, 2, 2, 3, 3], 2),
                    ([1, 2, 3, 4, 5, 6], 2), ([1, 1, 2, 3], 2), ([1, 2, 3, 3, 4, 5], 3),
                    ([1, 2, 3, 4], 3), ([8, 10, 12], 3), ([1, 2, 2, 3, 3, 4], 3),
                    ([0, 1000000000], 1), ([999999998, 1000000000, 999999999], 3),
                    ([4, 3, 2, 3, 4, 5, 6, 5], 4), ([0, 0, 1, 2, 3, 3], 2)]:
        show(hand, g)
    all_ = list(range(10000))
    shuffle(all_)
    print(f"0..9999 shuffled, one group of 10000: {b(is_n_straight_hand(all_, 10000))}")
    print(f"0..9999 shuffled, groups of 16: {b(is_n_straight_hand(all_, 16))}")
    print(f"0..9999 shuffled, groups of 3: {b(is_n_straight_hand(all_, 3))}")
    fours = []
    for g in range(2500):
        start = 1000000000 - 4 - (g % 50) * 3
        for j in range(4):
            fours.append(start + j)
    shuffle(fours)
    print(f"2500 overlapping groups of 4 near 10^9: {b(is_n_straight_hand(fours, 4))}")
    fours[0] += 1
    print(f"the same with one card moved up one: {b(is_n_straight_hand(fours, 4))}")
    ones = [7] * 10000
    print(f"10000 sevens, groups of 1: {b(is_n_straight_hand(ones, 1))}")
    print(f"10000 sevens, groups of 2: {b(is_n_straight_hand(ones, 2))}")
    trues = 0
    check = 0
    for _ in range(600):
        group_size = 1 + next_random() % 4
        groups = 1 + next_random() % 6
        kind = next_random() % 4
        hand = []
        if kind == 3:
            for _ in range(group_size * groups):
                hand.append(next_random() % 5)
        else:
            for _ in range(groups):
                start = next_random() % 8
                for j in range(group_size):
                    hand.append(start + j)
            if kind == 1:
                at = next_random() % len(hand)
                hand[at] = next_random() % 10
            elif kind == 2:
                hand.append(next_random() % 10)
        shuffle(hand)
        ok = is_n_straight_hand(hand, group_size)
        if ok:
            trues += 1
        check = (check * 31 + len(hand) * 2 + (1 if ok else 0)) % 1000000007
    print(f"600 random hands: {trues} split, checksum {check}")


main()
