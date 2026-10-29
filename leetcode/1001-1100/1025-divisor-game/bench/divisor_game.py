# LeetCode #1025: Divisor Game -- bench
# Mirrors ./divisor_game.kara; see ../README.md § Benchmarks.


def divisor_game(n):
    divisors = [[] for _ in range(n + 1)]
    for x in range(1, n // 2 + 1):
        m = 2 * x
        while m <= n:
            divisors[m].append(x)
            m += x
    wins = [False] * (n + 1)
    for m in range(2, n + 1):
        wins[m] = any(not wins[m - x] for x in divisors[m])
    return wins[n]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 100
    rounds = 100
    seed = [1025]
    games = [500 + next_random(seed) % 501 for _ in range(count)]
    wins = 0
    check = 0
    for _ in range(rounds):
        for n in games:
            alice = divisor_game(n)
            if alice:
                wins += 1
            check = (check * 131 + n * 2 + (1 if alice else 0)) % 1000000007
    print(f"{count} games of n from 500 to 1000, {rounds} rounds: Alice wins {wins}, checksum {check}")


main()
