# LeetCode #2225: Find Players With Zero or One Losses -- the benchmark's
# Python mirror of players.kara: a dict of losses, both lists sorted.


def find_winners(matches):
    losses = {}
    for winner, loser in matches:
        if winner not in losses:
            losses[winner] = 0
        losses[loser] = losses.get(loser, 0) + 1
    unbeaten = []
    once = []
    for player, count in losses.items():
        if count == 0:
            unbeaten.append(player)
        elif count == 1:
            once.append(player)
    unbeaten.sort()
    once.sort()
    return [unbeaten, once]


seed = 2225


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def draw_match():
    winner = wide_random() % 100000 + 1
    loser = wide_random() % 100000 + 1
    if loser == winner:
        loser = winner % 100000 + 1
    return [winner, loser]


def main():
    tournaments = [[draw_match() for _ in range(100000)] for _ in range(4)]
    listed = 0
    check = 0
    for _ in range(25):
        for t in range(4):
            # punch: one match is drawn again before each answer
            at = wide_random() % 100000
            tournaments[t][at] = draw_match()
            for lst in find_winners(tournaments[t]):
                listed += len(lst)
                check = (check * 31 + len(lst)) % 1000000007
                for p in lst:
                    check = (check * 31 + p) % 1000000007
    print(f"100 tournaments: {listed} players listed in all, checksum {check}")


main()
