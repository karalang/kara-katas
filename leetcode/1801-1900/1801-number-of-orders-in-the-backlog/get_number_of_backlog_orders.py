# LeetCode #1801: Number of Orders in the Backlog -- the ★ arm in Python:
# the buys in a heap that gives the highest price first, the sells in one
# that gives the lowest first, each order matched while it crosses.
import heapq


def get_number_of_backlog_orders(orders):
    buys = []
    sells = []
    for price, amount, kind in orders:
        if kind == 0:
            while amount > 0 and sells and sells[0][0] <= price:
                p, a = heapq.heappop(sells)
                if a > amount:
                    heapq.heappush(sells, (p, a - amount))
                    amount = 0
                else:
                    amount -= a
            if amount > 0:
                heapq.heappush(buys, (-price, amount))
        else:
            while amount > 0 and buys and -buys[0][0] >= price:
                p, a = heapq.heappop(buys)
                if a > amount:
                    heapq.heappush(buys, (p, a - amount))
                    amount = 0
                else:
                    amount -= a
            if amount > 0:
                heapq.heappush(sells, (price, amount))
    return (sum(a for _, a in buys) + sum(a for _, a in sells)) % 1000000007


seed = 1801


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    f = get_number_of_backlog_orders
    first = [[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]]
    second = [[7, 1000000000, 1], [15, 3, 0], [5, 999999995, 0], [5, 1, 1]]
    print(f"{f(first)} {f(second)}")
    edges = [[[5, 3, 1]], [[4, 2, 0], [6, 3, 1]], [[6, 3, 1], [6, 3, 0]], [[5, 4, 1], [5, 1, 0]],
             [[1, 1, 1], [2, 2, 1], [3, 3, 1], [9, 10, 0]], [[1, 1000000000, 0], [2, 1000000000, 0]]]
    print(" ".join(str(f(e)) for e in edges))
    rests = [[i + 1, 1000000000, 0] for i in range(100000)]
    wide = []
    for _ in range(100000):
        p = 1 + next_random() % 1000000000
        a = 1 + next_random() % 1000000000
        t = next_random() % 2
        wide.append([p, a, t])
    print(f"the most: {f(rests)} {f(wide)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        orders = []
        for _ in range(n):
            p = 1 + next_random() % 10
            a = 1 + next_random() % 10
            t = next_random() % 2
            orders.append([p, a, t])
        check = (check * 31 + f(orders)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
