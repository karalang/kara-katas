# Benchmark for #656: cheapest cost to the end, worked backwards, as the
# Kara ★ arm.

UNREACHABLE = (1 << 63) - 1


def cheapest_jump(coins, max_jump):
    n = len(coins)
    cost = [UNREACHABLE] * n
    nxt = [-1] * n
    if coins[n - 1] != -1:
        cost[n - 1] = coins[n - 1]
    for i in range(n - 2, -1, -1):
        if coins[i] == -1:
            continue
        last = min(i + max_jump, n - 1)
        for j in range(i + 1, last + 1):
            if cost[j] != UNREACHABLE and coins[i] + cost[j] < cost[i]:
                cost[i] = coins[i] + cost[j]
                nxt[i] = j
    path = []
    if cost[0] == UNREACHABLE:
        return path
    at = 0
    while at != -1:
        path.append(at + 1)
        at = nxt[at]
    return path


seed = 656


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs, rounds, n = 8, 40, 100000
    rows = []
    for _ in range(inputs):
        coins = []
        for i in range(n):
            if i > 0 and next_random() % 10 == 0:
                coins.append(-1)
            else:
                coins.append(next_random() % 101)
        rows.append(coins)
    steps = 0
    checksum = 0
    for r in range(rounds):
        coins = rows[(r * 3) % inputs]
        path = cheapest_jump(coins, 100)
        cost = 0
        for p in path:
            cost += coins[p - 1]
            checksum = (checksum * 31 + p) % 1000000007
        steps += len(path)
        checksum = (checksum * 31 + cost) % 1000000007
    print(f"{inputs} rows of {n}, {rounds} rounds: {steps} steps, checksum {checksum}")


main()
