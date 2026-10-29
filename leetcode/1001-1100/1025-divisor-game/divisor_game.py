# LeetCode #1025: Divisor Game -- parity
# Mirrors divisor_game.kara (the ★ arm) and prints the same output.


def divisor_game(n):
    return n % 2 == 0


seed = 1025


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [2, 3]:
        print(f"n = {n} -> {'true' if divisor_game(n) else 'false'}")
    line = "".join("A" if divisor_game(n) else "B" for n in range(1, 61))
    print(f"n = 1 to 60: {line}")
    groups = [(500, 10), (300, 50), (200, 100), (60, 300), (20, 600), (10, 1000)]
    for count, top in groups:
        wins = 0
        check = 0
        for _ in range(count):
            n = 1 + next_random() % top
            alice = divisor_game(n)
            if alice:
                wins += 1
            check = (check * 131 + n * 2 + (1 if alice else 0)) % 1000000007
        print(f"{count} games, n up to {top}: Alice wins {wins}, checksum {check}")
    t = lambda b: "true" if b else "false"
    print(f"n = 1000 -> {t(divisor_game(1000))}, n = 999 -> {t(divisor_game(999))}")


main()
