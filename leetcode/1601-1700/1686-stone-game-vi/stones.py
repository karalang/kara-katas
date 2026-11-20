# LeetCode #1686: Stone Game VI -- mirrors stones.kara, the ★ arm: the
# stones by their worth to both players.


def stone_game(alice, bob):
    order = sorted(range(len(alice)), key=lambda i: -(alice[i] + bob[i]))
    difference = 0
    for turn, i in enumerate(order):
        if turn % 2 == 0:
            difference += alice[i]
        else:
            difference -= bob[i]
    return (difference > 0) - (difference < 0)


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, seed):
    wins = [0, 0, 0]
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        alice, bob = [], []
        for _ in range(n):
            alice.append(seed.next() % top + 1)
            bob.append(seed.next() % top + 1)
        answer = stone_game(alice, bob)
        wins[answer + 1] += 1
        check = (check * 31 + answer + 2) % 1000000007
    print(f"{count} games of up to {most} stones up to {top}: Alice {wins[2]}, Bob {wins[0]}, draws {wins[1]}, checksum {check}")


def main():
    print(stone_game([1, 3], [2, 1]))
    print(stone_game([1, 2], [3, 1]))
    print(stone_game([2, 4, 3], [1, 6, 7]))
    print(stone_game([5], [5]))
    print(stone_game([1, 1], [1, 1]))
    seed = Seed(1686)
    batch(3000, 10, 5, seed)
    batch(300, 1000, 100, seed)
    batch(10, 100000, 100, seed)


main()
