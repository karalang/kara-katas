# Benchmark for #837: New 21 Game -- the ★ arm (forward, with a sliding window).
#
# Mirrors new21_game.kara: p[i] is the chance that Alice's points are ever
# exactly i, the sum over max_pts of the chances of the totals in the last
# max_pts below i at which she still draws, kept in a running window.


def new21_game(n, k, max_pts):
    if k == 0 or n >= k - 1 + max_pts:
        return 1.0
    w = float(max_pts)
    p = [0.0] * (n + 1)
    p[0] = 1.0
    window = 1.0
    answer = 0.0
    for i in range(1, n + 1):
        p[i] = window / w
        if i < k:
            window += p[i]
        else:
            answer += p[i]
        gone = i - max_pts
        if gone >= 0 and gone < k:
            window -= p[gone]
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 64 games drawn once, each with n from 5000 to 10^4, k from n / 2 to
    # n, and maxPts large enough that Alice can go past n, so that no game
    # takes the early return. Each round plays the next game.
    count = 64
    rounds = 25000
    seed = [837]
    games = []
    for _ in range(count):
        n = 5000 + next_random(seed) % 5001
        k = n // 2 + next_random(seed) % (n - n // 2 + 1)
        least = n - k + 2
        max_pts = least + next_random(seed) % (10001 - least)
        games.append((n, k, max_pts))
    s = 0.0
    for round_ in range(rounds):
        n, k, max_pts = games[round_ % count]
        s += new21_game(n, k, max_pts)
    print(f"{rounds} rounds of {count} games: sum {s:.6f}")


main()
