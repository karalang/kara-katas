# LeetCode #877 bench: Python mirror of stone_game.kara (the ★ arm, the
# best margin of every run of piles) on the same 1,000 games.


def stone_game(piles):
    n = len(piles)
    margin = [[piles[i] if i == j else 0 for j in range(n)] for i in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            margin[i][j] = max(piles[i] - margin[i + 1][j], piles[j] - margin[i][j - 1])
    return margin[0][n - 1] > 0


seed = 877


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_piles(limit):
    piles = []
    total = 0
    for _ in range(500):
        p = next_random() % limit + 1
        piles.append(p)
        total += p
    if total % 2 == 0:
        piles[0] = piles[0] - 1 if piles[0] == limit else piles[0] + 1
    return piles


def main():
    rows = [random_piles(500 if k % 2 == 0 else 3) for k in range(20)]
    wins = 0
    check = 0
    for k in range(1000):
        answer = stone_game(rows[k % 20])
        if answer:
            wins += 1
        check = (check * 3 + (1 if answer else 2)) % 1000000007
    print(f"1000 games of 500 piles: Alice wins {wins}, checksum {check}")


main()
