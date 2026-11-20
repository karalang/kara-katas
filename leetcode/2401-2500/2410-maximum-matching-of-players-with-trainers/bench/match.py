# LeetCode #2410: Maximum Matching of Players With Trainers -- the bench,
# the ★ arm in Python: both lists sorted, each trainer upward taking the
# weakest player not yet matched if it is strong enough.

seed = 2410


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def match_players_and_trainers(players, trainers):
    p = sorted(players)
    matched = 0
    for capacity in sorted(trainers):
        if matched < len(p) and p[matched] <= capacity:
            matched += 1
    return matched


def main():
    cases = []
    for i in range(10):
        players = [1 + (next_random() * 32768 + next_random()) % 1000000000 for _ in range(100000)]
        trainers = [1 + (next_random() * 32768 + next_random()) % 900000000 + 10000000 * i for _ in range(100000)]
        cases.append((players, trainers))
    check = 0
    for p in range(5):
        for players, trainers in cases:
            check = (check * 31 + match_players_and_trainers(players, trainers) + p) % 1000000007
    print(f"5 passes over 10 cases of 10^5 players and trainers: checksum {check}")


main()
