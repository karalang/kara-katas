# LeetCode #1140: Stone Game II -- mirrors stone_game_ii.kara (the ★ arm).


def stone_game_ii(piles):
    n = len(piles)
    left = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        left[i] = left[i + 1] + piles[i]
    best = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for m in range(1, n + 1):
            if i + 2 * m >= n:
                best[i][m] = left[i]
            else:
                most = 0
                for x in range(1, 2 * m + 1):
                    most = max(most, left[i] - best[i + x][max(m, x)])
                best[i][m] = most
    return best[0][1]


seed = 1140


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_piles(n, most):
    return [next_random() % most + 1 for _ in range(n)]


def main():
    print(f"example 1: {stone_game_ii([2, 7, 9, 4, 4])}")
    print(f"example 2: {stone_game_ii([1, 2, 3, 4, 5, 100])}")
    print(f"one pile: {stone_game_ii([5])}")
    print(f"two piles: {stone_game_ii([3, 9])}")
    print(f"a big pile third: {stone_game_ii([1, 1, 100])}")
    print(f"a big pile fifth: {stone_game_ii([1, 1, 1, 1, 100])}")
    print(f"seven equal piles: {stone_game_ii([4] * 7)}")
    total = 0
    check = 0
    for i in range(2000):
        n = next_random() % 30 + 1
        most = 10 if i % 3 == 2 else 10000
        piles = random_piles(n, most)
        answer = stone_game_ii(piles)
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"2000 random rows: answers total {total}, checksum {check}")
    print(f"100 piles of 10000: {stone_game_ii([10000] * 100)}")
    print(f"100 piles rising: {stone_game_ii(list(range(1, 101)))}")
    print(f"100 random piles: {stone_game_ii(random_piles(100, 10000))}")


main()
