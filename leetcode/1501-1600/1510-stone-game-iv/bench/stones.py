# LeetCode #1510: Stone Game IV -- the bench: 40 piles of 50000 to 100000
# stones, each answered by the ★ arm.


def winner_square_game(n):
    wins = [False] * (n + 1)
    for pile in range(1, n + 1):
        k = 1
        while k * k <= pile:
            if not wins[pile - k * k]:
                wins[pile] = True
                break
            k += 1
    return wins[n]


seed = 1510


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


wins = 0
check = 0
for _ in range(40):
    hi = next_random() * 32768
    n = 50000 + (hi + next_random()) % 50001
    w = winner_square_game(n)
    if w:
        wins += 1
    check = (check * 31 + (n if w else 0) + 1) % 1000000007
print(f"40 piles of 50000 to 100000 stones: Alice wins {wins}, checksum {check}")
