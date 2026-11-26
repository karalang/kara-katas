# Mirror of stone_game_iii.kara: how far ahead the player to move can end,
# from the last stone back.


def stone_game_iii(stone_value):
    n = len(stone_value)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        taken = 0
        best[i] = -2**31
        for k in range(1, 4):
            if i + k > n:
                break
            taken += stone_value[i + k - 1]
            best[i] = max(best[i], taken - best[i + k])
    return "Alice" if best[0] > 0 else "Bob" if best[0] < 0 else "Tie"


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, lo, hi):
    return [lo + next_random() % (hi - lo + 1) for _ in range(n)]


def main():
    global seed
    print(" ".join(stone_game_iii(v) for v in [[1, 2, 3, 7], [1, 2, 3, -9], [1, 2, 3, 6], [-1], [0], [-1, -2, -3]]))
    seed = 1406
    top = [1000] * 50000
    bottom = [-1000] * 50000
    big = drawn(50000, -1000, 1000)
    print(f"5 * 10^4 stones: {stone_game_iii(top)} {stone_game_iii(bottom)} {stone_game_iii(big)}")
    wins = [0, 0, 0]
    check = 0
    for i in range(3000):
        n = 1 + next_random() % 40
        lim = 1000 if i % 2 == 0 else 3
        winner = stone_game_iii(drawn(n, -lim, lim))
        k = {"Alice": 0, "Bob": 1, "Tie": 2}[winner]
        wins[k] += 1
        check = (check * 131 + k + 1) % 1000000007
    print(f"3000 random rows: Alice {wins[0]}, Bob {wins[1]}, Tie {wins[2]}, checksum {check}")


main()
