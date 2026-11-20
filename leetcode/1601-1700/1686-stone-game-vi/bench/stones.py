# LeetCode #1686: Stone Game VI -- the bench's Python mirror: the ★ arm on
# 50 random games of 100000 stones, all drawn first, each answered 10 times.


def stone_game(alice, bob):
    order = sorted(range(len(alice)), key=lambda i: -(alice[i] + bob[i]))
    difference = 0
    for turn, i in enumerate(order):
        if turn % 2 == 0:
            difference += alice[i]
        else:
            difference -= bob[i]
    return (difference > 0) - (difference < 0)


seed = 1686


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 50, 100000, 10
    games = []
    for _ in range(count):
        alice, bob = [], []
        for _ in range(size):
            alice.append(next_random() % 100 + 1)
            bob.append(next_random() % 100 + 1)
        games.append((alice, bob))
    wins = [0, 0, 0]
    check = 0
    for r in range(rounds):
        for alice, bob in games:
            answer = stone_game(alice, bob)
            wins[answer + 1] += 1
            check = (check * 31 + answer + 2 + r) % 1000000007
    print(f"{count} games of {size} stones, {rounds} rounds: Alice {wins[2]}, Bob {wins[0]}, draws {wins[1]}, checksum {check}")


main()
