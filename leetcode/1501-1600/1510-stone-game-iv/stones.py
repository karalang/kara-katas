# LeetCode #1510: Stone Game IV -- the Python mirror of the ★ arm: a pile
# wins for the player to move when some square taken leaves a pile that
# loses; filled from the empty pile upward.


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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(b):
    return "true" if b else "false"


for n in [1, 2, 4, 7, 17, 8, 100000]:
    print(f"n = {n} -> {show(winner_square_game(n))}")
wins = 0
check = 0
for n in range(1, 601):
    w = winner_square_game(n)
    if w:
        wins += 1
    check = mix(check, n if w else 0)
print(f"n from 1 to 600: Alice wins {wins}, checksum {check}")
check = 0
for _ in range(3):
    hi = next_random() * 32768
    n = (hi + next_random()) % 100000 + 1
    check = mix(check, n if winner_square_game(n) else 0)
print(f"3 random n up to 100000: checksum {check}")
