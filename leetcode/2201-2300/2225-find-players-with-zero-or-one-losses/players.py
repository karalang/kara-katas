# LeetCode #2225: Find Players With Zero or One Losses -- mirror of
# players.kara: a dict from player to losses, then the players with 0
# and with 1 collected and sorted. O(m log m).


def find_winners(matches):
    losses = {}
    for winner, loser in matches:
        if winner not in losses:
            losses[winner] = 0
        losses[loser] = losses.get(loser, 0) + 1
    unbeaten = sorted(p for p, c in losses.items() if c == 0)
    once = sorted(p for p, c in losses.items() if c == 1)
    return [unbeaten, once]


seed = 2225


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


# m matches among players 1 to players, no player against itself and
# no match twice
def draw_matches(m, players):
    seen = set()
    matches = []
    tries = 0
    while len(matches) < m and tries < 4 * m:
        tries += 1
        winner = wide_random() % players + 1
        loser = wide_random() % players + 1
        if winner != loser and winner * 200003 + loser not in seen:
            seen.add(winner * 200003 + loser)
            matches.append([winner, loser])
    return matches


def show(matches):
    print(f"{matches} -> {find_winners(matches)}")


def main():
    # LeetCode's two examples, then four more: one match, a cycle of
    # three, a player losing twice, and a chain
    show([[1, 3], [2, 3], [3, 6], [5, 6], [5, 7], [4, 5], [4, 8], [4, 9], [10, 4], [10, 9]])
    show([[2, 3], [1, 3], [5, 4], [6, 4]])
    show([[7, 2]])
    show([[1, 2], [2, 3], [3, 1]])
    show([[4, 9], [5, 9], [9, 6]])
    show([[1, 2], [2, 3], [3, 4], [4, 5]])
    # 3000 random tournaments of 1 to 30 matches among 5, 30 and 10^5
    # players in turn
    check = 0
    for c in range(3000):
        m = next_random() % 30 + 1
        matches = draw_matches(m, [5, 30, 100000][c % 3])
        for lst in find_winners(matches):
            check = (check * 31 + len(lst)) % 1000000007
            for p in lst:
                check = (check * 31 + p) % 1000000007
    print(f"3000 tournaments: checksum {check}")
    # the constraints' largest: 10^5 matches among 10^5 players
    wide = draw_matches(100000, 100000)
    answer = find_winners(wide)
    s = 0
    for p in answer[1]:
        s = (s * 31 + p) % 1000000007
    print(f"10^5 matches: {len(answer[0])} unbeaten, {len(answer[1])} beaten once, checksum {s}")


main()
