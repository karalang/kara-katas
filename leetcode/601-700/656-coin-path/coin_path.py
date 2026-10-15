# LeetCode #656: Coin Path -- cheapest cost to the end, worked backwards.
# Mirrors the ★ arm (coin_path.kara) and its test harness.

UNREACHABLE = (1 << 63) - 1


def cheapest_jump(coins, max_jump):
    n = len(coins)
    cost = [UNREACHABLE] * n
    nxt = [-1] * n
    if coins[n - 1] != -1:
        cost[n - 1] = coins[n - 1]
    for i in range(n - 2, -1, -1):
        if coins[i] != -1:
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(coins, max_jump):
    path = cheapest_jump(coins, max_jump)
    cells = ",".join(str(c) for c in coins)
    steps = ",".join(str(p) for p in path)
    print(f"[{cells}], {max_jump} -> [{steps}]")


def random_coins(n, top, blocked):
    coins = []
    for i in range(n):
        if i > 0 and next_random() % 100 < blocked:
            coins.append(-1)
        else:
            coins.append(next_random() % (top + 1))
    return coins


def summary(coins, path):
    cost = 0
    s = 0
    for p in path:
        cost += coins[p - 1]
        s = (s * 31 + p) % 1000000007
    return len(path), cost, s


def main():
    global seed
    show([1, 2, 4, -1, 2], 2)
    show([1, 2, 4, -1, 2], 1)
    show([0], 1)
    show([3, 1, -1], 2)
    show([0, 0, 0, 0, 0], 3)
    show([1, 0, 0, 0, 9, 1], 4)
    show([0, 1, 0, 0], 3)
    seed = 656
    found = steps = total = s = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        jump = 1 + next_random() % 6
        coins = random_coins(n, 100, 20)
        length, cost, check = summary(coins, cheapest_jump(coins, jump))
        if length > 0:
            found += 1
        steps += length
        total += cost
        s = (s * 7 + check) % 1000000007
    print(f"300 random rows: {found} with a path, {steps} steps, cost {total}, checksum {s}")
    coins = random_coins(1000, 100, 30)
    length, cost, check = summary(coins, cheapest_jump(coins, 100))
    print(f"1000 random, jump 100: {length} steps, cost {cost}, checksum {check}")
    coins = [0] * 1000
    length, cost, check = summary(coins, cheapest_jump(coins, 100))
    print(f"1000 free, jump 100: {length} steps, cost {cost}, checksum {check}")
    coins = random_coins(1000, 100, 0)
    coins[500] = -1
    length, cost, check = summary(coins, cheapest_jump(coins, 1))
    print(f"1000 with one blocked, jump 1: {length} steps, cost {cost}, checksum {check}")


main()
