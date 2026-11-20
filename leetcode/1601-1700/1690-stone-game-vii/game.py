# LeetCode #1690: Stone Game VII -- mirrors game.kara, the ★ arm: one row
# of the table at a time.


def stone_game(stones):
    n = len(stones)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]
    best = [0] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            take_left = prefix[j + 1] - prefix[i + 1] - best[j]
            take_right = prefix[j] - prefix[i] - best[j - 1]
            best[j] = max(take_left, take_right)
    return best[n - 1]


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % (most - 1) + 2
        stones = [seed.next() % top + 1 for _ in range(n)]
        answer = stone_game(stones)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} rows of up to {most} stones up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(stone_game([5, 3, 1, 4, 2]))
    print(stone_game([7, 90, 5, 1, 100, 10, 10, 2]))
    print(stone_game([1, 1]))
    print(stone_game([1000, 1]))
    seed = Seed(1690)
    batch(3000, 10, 10, seed)
    batch(300, 100, 1000, seed)
    batch(30, 1000, 1000, seed)


main()
