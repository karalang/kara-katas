# LeetCode 787 — Cheapest Flights Within K Stops: the bench, in Python.
# Mirrors find_cheapest_price.kara: Bellman-Ford for k + 1 rounds, each
# round reading a fresh copy of the costs, over the same 64 networks.
import sys

UNREACHED = sys.maxsize


def find_cheapest_price(n, flights, src, dst, k):
    cost = [UNREACHED] * n
    cost[src] = 0
    for _ in range(k + 1):
        before = cost[:]
        for frm, to, price in flights:
            if before[frm] != UNREACHED and before[frm] + price < cost[to]:
                cost[to] = before[frm] + price
    return -1 if cost[dst] == UNREACHED else cost[dst]


seed = 787


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    networks = []
    for _ in range(64):
        taken = [False] * 10000
        flights = []
        while len(flights) < 1000:
            frm = next_random() % 100
            to = next_random() % 100
            if frm != to and not taken[frm * 100 + to]:
                taken[frm * 100 + to] = True
                flights.append([frm, to, 1 + next_random() % 10000])
        networks.append(flights)
    rounds = 20000
    found = 0
    check = 0
    for r in range(rounds):
        src = next_random() % 100
        dst = (src + 1 + next_random() % 99) % 100
        k = next_random() % 100
        answer = find_cheapest_price(100, networks[r % 64], src, dst, k)
        if answer != -1:
            found += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{rounds} rounds of 100-city networks: {found} with a way, checksum {check}")


main()
