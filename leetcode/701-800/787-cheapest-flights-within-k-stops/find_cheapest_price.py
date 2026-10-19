# LeetCode 787 — Cheapest Flights Within K Stops, Bellman-Ford for k + 1
# rounds.
# Mirrors find_cheapest_price.kara (the ★ arm) and its harness.

UNREACHED = 2**63 - 1


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


def random_flights(n, m, top):
    taken = set()
    flights = []
    while len(flights) < m:
        frm = next_random() % n
        to = next_random() % n
        if frm != to and frm * n + to not in taken:
            taken.add(frm * n + to)
            flights.append([frm, to, 1 + next_random() % top])
    return flights


def text(v):
    if isinstance(v, list):
        return "[" + ", ".join(text(x) for x in v) + "]"
    return str(v)


def show(n, flights, src, dst, k):
    answer = find_cheapest_price(n, flights, src, dst, k)
    print(f"n = {n}, flights = {text(flights)}, {src} to {dst}, k = {k} -> {answer}")


def main():
    show(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1)
    show(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1)
    show(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0)
    show(3, [[0, 1, 100], [1, 0, 100]], 0, 2, 2)
    show(4, [[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]], 0, 3, 1)
    show(5, [[0, 1, 5], [1, 2, 5], [0, 3, 2], [3, 1, 2], [1, 4, 1]], 0, 2, 2)
    chain = [[i, i + 1, 1] for i in range(99)] + [[0, 99, 1000]]
    for k in [0, 97, 98, 99]:
        answer = find_cheapest_price(100, chain, 0, 99, k)
        print(f"a chain of 100 cities and one direct flight, k = {k} -> {answer}")
    found = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 99
        m = next_random() % min(n * (n - 1) // 2, 5 * n) + 1
        flights = random_flights(n, m, 10000)
        src = next_random() % n
        dst = next_random() % n
        if dst == src:
            dst = (dst + 1) % n
        k = next_random() % n
        answer = find_cheapest_price(n, flights, src, dst, k)
        if answer != -1:
            found += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"300 random networks: {found} with a way, checksum {check}")


main()
