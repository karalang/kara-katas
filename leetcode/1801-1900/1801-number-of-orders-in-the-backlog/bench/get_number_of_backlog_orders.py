# LeetCode #1801: Number of Orders in the Backlog -- the bench in Python: the
# ★ arm over 400 random lists of 500 orders built once, 10000 calls.
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
    lists = []
    for _ in range(400):
        orders = []
        for _ in range(500):
            p = 1 + next_random() % 1000
            a = 1 + next_random() % 1000
            t = next_random() % 2
            orders.append((p, a, t))
        lists.append(orders)
    check = 0
    for call in range(10000):
        orders = lists[(check + call) % 400]
        check = (check * 31 + get_number_of_backlog_orders(orders)) % 1000000007
    print(f"10000 calls over 400 lists of 500 orders: checksum {check}")


main()
