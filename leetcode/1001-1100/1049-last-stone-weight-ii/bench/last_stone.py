# LeetCode #1049: Last Stone Weight II -- Python mirror of
# bench/last_stone.kara.


def last_stone_weight_ii(stones):
    total = sum(stones)
    half = total // 2
    made = [False] * (half + 1)
    made[0] = True
    for s in stones:
        t = half
        while t >= s:
            if made[t - s]:
                made[t] = True
            t -= 1
    best = half
    while not made[best]:
        best -= 1
    return total - 2 * best


seed = 1049


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists, count, rounds = 1000, 30, 10
    all_lists = [[next_random() % 100 + 1 for _ in range(count)] for _ in range(lists)]
    total = 0
    check = 0
    for _ in range(rounds):
        for stones in all_lists:
            answer = last_stone_weight_ii(stones)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{lists} lists of {count} stones, {rounds} rounds: total {total}, checksum {check}")


main()
