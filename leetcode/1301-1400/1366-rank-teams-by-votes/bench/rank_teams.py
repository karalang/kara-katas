# LeetCode #1366 bench -- Python: how many votes put each team in each
# place counted, and the teams sorted by those counts, then by letter.


def rank_teams(votes):
    places = len(votes[0])
    counts = [[0] * places for _ in range(26)]
    for vote in votes:
        for place, team in enumerate(vote.encode()):
            counts[team - 65][place] += 1
    teams = sorted(votes[0].encode(), key=lambda t: ([-c for c in counts[t - 65]], t))
    return bytes(teams).decode()


seed = 1366


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 elections of 1000 votes over all 26 teams, the constraints' most,
    # built once; then 3000 rounds, each swapping two places of one vote,
    # all drawn from the checksum so far, ranking that election and
    # folding the ranking into the checksum
    elections = []
    for _ in range(20):
        votes = []
        for _ in range(1000):
            vote = list(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            for i in range(1, 26):
                j = next_random() % (i + 1)
                vote[i], vote[j] = vote[j], vote[i]
            votes.append(bytes(vote).decode())
        elections.append(votes)
    check = 0
    for r in range(3000):
        e = check % 20
        v = (check // 20) % 1000
        i, j = (check // 20000) % 26, (check // 520000) % 26
        vote = list(elections[e][v].encode())
        vote[i], vote[j] = vote[j], vote[i]
        elections[e][v] = bytes(vote).decode()
        ranked = rank_teams(elections[e])
        for b in ranked.encode():
            check = (check * 31 + b) % 1000000007
        check = (check + r) % 1000000007
    print(f"3000 rounds over 20 elections of 1000 votes: checksum {check}")


main()
