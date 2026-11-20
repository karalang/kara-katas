# LeetCode #2347: Best Poker Hand -- the Python mirror of the ★ arm: a
# flush when every suit equals the first; otherwise the most cards of one
# rank, counted in a table of 14, names the hand.


def best_hand(ranks, suits):
    if all(s == suits[0] for s in suits):
        return "Flush"
    count = [0] * 14
    most = 0
    for r in ranks:
        count[r] += 1
        most = max(most, count[r])
    if most >= 3:
        return "Three of a Kind"
    if most == 2:
        return "Pair"
    return "High Card"


SEED = [2347]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


NAMES = ["Flush", "Three of a Kind", "Pair", "High Card"]


def main():
    print(best_hand([13, 2, 3, 1, 9], list("aaaaa")))
    print(best_hand([4, 4, 2, 4, 4], list("daabc")))
    print(best_hand([10, 10, 2, 12, 9], list("abcad")))
    print(best_hand([1, 5, 9, 12, 13], list("abcda")))
    print(best_hand([7, 7, 7, 3, 3], list("abcab")))
    print(best_hand([2, 2, 3, 3, 13], list("abacd")))
    # 2000 random hands of five different cards, their suits drawn from
    # the first one to four letters and their ranks from the first five to
    # thirteen
    check = 0
    counts = [0, 0, 0, 0]
    for _ in range(2000):
        suit_spread = 1 + next_random() % 4
        rank_spread = 5 + next_random() % 9
        ranks = []
        suits = []
        while len(ranks) < 5:
            r = 1 + next_random() % rank_spread
            s = chr(97 + next_random() % suit_spread)
            if not any(ranks[i] == r and suits[i] == s for i in range(len(ranks))):
                ranks.append(r)
                suits.append(s)
        k = NAMES.index(best_hand(ranks, suits))
        check = (check * 31 + k + 1) % 1000000007
        counts[k] += 1
    print(f"2000 hands: checksum {check}, flush {counts[0]}, three {counts[1]}, pair {counts[2]}, high card {counts[3]}")


main()
