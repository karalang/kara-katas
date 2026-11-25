# LeetCode #1366: Rank Teams by Votes -- Python mirror of the ★ arm: how
# many votes put each team in each place counted, and the teams sorted by
# those counts, first place's first, then by letter.


def rank_teams(votes):
    places = len(votes[0])
    counts = {team: [0] * places for team in votes[0]}
    for vote in votes:
        for place, team in enumerate(vote):
            counts[team][place] += 1
    teams = sorted(votes[0], key=lambda t: ([-c for c in counts[t]], t))
    return "".join(teams)


seed = 1366


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled(letters):
    out = list(letters)
    for i in range(1, len(out)):
        j = next_random() % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def main():
    examples = [
        ["ABC", "ACB", "ABC", "ACB", "ACB"],
        ["WXYZ", "XYZW"],
        ["ZMNAGUEDSJYLBOPHRQICWFXTVK"],
        ["BCA", "CAB", "CBA", "ABC", "ACB", "BAC"],
        ["M", "M", "M", "M"],
    ]
    print(" ".join(rank_teams(v) for v in examples))
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    check = 0
    first_a = 0
    for _ in range(2000):
        a = next_random()
        b = next_random()
        teams = 1 + a % (4 if b % 2 == 0 else 26)
        count = 1 + next_random() % 40
        chosen = shuffled(alphabet)[:teams]
        votes = ["".join(shuffled(chosen)) for _ in range(count)]
        ranked = rank_teams(votes)
        if ranked.startswith("A"):
            first_a += 1
        check = (check * 131 + len(ranked)) % 1000000007
        for ch in ranked.encode():
            check = (check * 31 + ch) % 1000000007
    print(f"2000 random elections: {first_a} won by A, checksum {check}")


main()
