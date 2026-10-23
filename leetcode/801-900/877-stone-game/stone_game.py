# LeetCode #877: Stone Game -- Python mirror of the ★ arm (the best
# margin of every run of piles) and its test harness; prints the same
# output as stone_game.kara.


def stone_game(piles):
    n = len(piles)
    margin = [[piles[i] if i == j else 0 for j in range(n)] for i in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            margin[i][j] = max(piles[i] - margin[i + 1][j], piles[j] - margin[i][j - 1])
    return margin[0][n - 1] > 0


# ---- test harness ----------------------------------------------------------

seed = 877


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_piles(n, limit):
    piles = []
    total = 0
    for _ in range(n):
        p = next_random() % limit + 1
        piles.append(p)
        total += p
    if total % 2 == 0:
        i = next_random() % n
        piles[i] = piles[i] - 1 if piles[i] == limit else piles[i] + 1
    return piles


def show(piles):
    text = [str(p) for p in piles]
    shown = f"{text[0]}, {text[1]}, ... ({len(text)} piles)" if len(text) > 8 else ", ".join(text)
    print(f"piles = [{shown}] -> {'true' if stone_game(piles) else 'false'}")


def main():
    show([5, 3, 4, 5])
    show([3, 7, 2, 3])
    show([1, 2])
    show([2, 1])
    show([1, 100, 2, 1])
    show([500, 1, 1, 1])
    show([1, 1, 1, 500])
    show([2, 9, 1, 1, 1, 7])
    show([500 if i == 0 else 499 + i % 2 for i in range(500)])
    wins = 0
    check = 0
    for k in range(100):
        n = 2 * (k + 1) if k < 20 else 2 * (next_random() % 250 + 1)
        limit = 500 if k % 2 == 0 else 3
        answer = stone_game(random_piles(n, limit))
        if answer:
            wins += 1
        check = (check * 3 + (1 if answer else 2)) % 1000000007
    print(f"100 games of 2 to 500 piles: Alice wins {wins}, checksum {check}")


main()
