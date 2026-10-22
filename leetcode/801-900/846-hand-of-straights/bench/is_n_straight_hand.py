# Benchmark for #846: Hand of Straights -- Python twin of the Kāra open-groups
# arm (sorted runs and a queue of open groups).
from collections import deque


def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size != 0:
        return False
    cards = sorted(hand)
    started = deque()
    open_ = 0
    last = 0
    i = 0
    n = len(cards)
    while i < n:
        value = cards[i]
        count = 0
        while i < n and cards[i] == value:
            count += 1
            i += 1
        if open_ > 0 and (value != last + 1 or count < open_):
            return False
        started.append(count - open_)
        last = value
        open_ = count
        if len(started) == group_size:
            open_ -= started.popleft()
    return open_ == 0


seed = 846


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 3000
    n = 10000
    sizes = [1, 2, 4, 5, 10, 16, 100, 1000]
    hands = []
    group_sizes = []
    for g in range(count):
        group_size = sizes[g % 8]
        window = 1 + next_random() % 20000
        hand = []
        while len(hand) < n:
            start = 999000000 + next_random() % window
            for j in range(group_size):
                hand.append(start + j)
        for i in range(n):
            j = i + next_random() % (n - i)
            hand[i], hand[j] = hand[j], hand[i]
        if g % 4 == 3:
            at = next_random() % n
            hand[at] += 1
        hands.append(hand)
        group_sizes.append(group_size)
    splits = 0
    checksum = 0
    for round_ in range(rounds):
        ok = is_n_straight_hand(hands[round_ % count], group_sizes[round_ % count])
        if ok:
            splits += 1
        checksum = (checksum * 31 + round_ % count + (1 if ok else 0)) % 1000000007
    print(f"{rounds} rounds of {count} hands: {splits} split, checksum {checksum}")


main()
