# LeetCode #1690: Stone Game VII -- the bench's Python mirror: the ★ arm on
# 40 random rows of 1000 stones, all drawn first, each answered 4 times.


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


seed = 1690


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 40, 1000, 4
    rows = [[next_random() % 1000 + 1 for _ in range(size)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for stones in rows:
            answer = stone_game(stones)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} rows of {size} stones, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
