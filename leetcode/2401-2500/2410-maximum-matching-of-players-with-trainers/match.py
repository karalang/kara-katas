# LeetCode #2410: Maximum Matching of Players With Trainers -- the mirror
# of the ★ arm: both lists sorted, each trainer upward taking the weakest
# player not yet matched if it is strong enough.

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


def values(n, top):
    return [1 + (next_random() * 32768 + next_random()) % top for _ in range(n)]


def main():
    print(match_players_and_trainers([4, 7, 9], [8, 2, 5, 8]))
    print(match_players_and_trainers([1, 1, 1], [10]))
    print(f"{match_players_and_trainers([5], [4])} {match_players_and_trainers([5], [5])}")
    print(match_players_and_trainers([7, 8, 9], [1, 2, 3, 4, 5, 6]))
    players = values(100000, 1000000000)
    trainers = values(100000, 1000000000)
    print(match_players_and_trainers(players, trainers))
    weak = values(100000, 500000000)
    strong = [t + 250000000 for t in values(50000, 500000000)]
    print(match_players_and_trainers(weak, strong))
    check = 0
    total = 0
    for _ in range(2000):
        p = values(1 + next_random() % 20, 30)
        t = values(1 + next_random() % 20, 30)
        a = match_players_and_trainers(p, t)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
