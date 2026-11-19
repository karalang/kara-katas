# LeetCode #1626: Best Team With No Conflicts -- the Python mirror of
# team.kara (★).
#
# Sorted by age, then score, a team has no conflict exactly when its
# scores never fall along that order: the best team ending at each player
# is its score plus the best ending at an earlier player scoring no higher.


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top_score, top_age):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        scores = []
        ages = []
        for _ in range(n):
            scores.append(next_random() % top_score + 1)
            ages.append(next_random() % top_age + 1)
        got = best_team_score(scores, ages)
        total += got
        check = mix(check, got)
    print(f"{count} teams of up to {most} players: best scores sum to {total}, checksum {check}")


def main():
    global seed
    print(best_team_score([1, 3, 5, 10, 15], [1, 2, 3, 4, 5]))
    print(best_team_score([4, 5, 6, 5], [2, 1, 2, 1]))
    print(best_team_score([1, 2, 3, 5], [8, 9, 10, 1]))
    print(best_team_score([7], [30]))
    print(best_team_score([9, 2, 7, 4], [5, 5, 5, 5]))
    seed = 1626
    batch(3000, 10, 10, 5)
    batch(300, 100, 1000, 100)
    batch(10, 1000, 30000, 1000)


main()
