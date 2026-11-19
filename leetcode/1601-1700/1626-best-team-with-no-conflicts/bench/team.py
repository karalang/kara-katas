# LeetCode #1626: Best Team With No Conflicts -- the bench in Python,
# mirroring team.kara: sorted by (age, score), the best team ending at
# each player from every earlier player scoring no higher.

seed = 1626


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def best_team_score(scores, ages):
    players = sorted(zip(ages, scores))
    n = len(players)
    best = [0] * n
    for i in range(n):
        score = players[i][1]
        best[i] = score
        for j in range(i):
            if players[j][1] <= score:
                best[i] = max(best[i], best[j] + score)
    return max(best)


def main():
    teams = []
    for _ in range(100):
        scores = []
        ages = []
        for _ in range(1000):
            high = next_random()
            scores.append((high * 32768 + next_random()) % 1000000 + 1)
            ages.append(next_random() % 1000 + 1)
        teams.append((scores, ages))
    check = 0
    total = 0
    for scores, ages in teams:
        got = best_team_score(scores, ages)
        total += got
        check = (check * 31 + got + 1) % 1000000007
    print(f"100 teams of 1000 players: best scores sum to {total}, checksum {check}")


main()
