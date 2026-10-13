# LeetCode #502: IPO -- Python mirror of the ★ arm (projects sorted by
# capital, profits in a heap); see ipo.kara. heapq is smallest-first,
# so the heap holds negated profits.
import heapq


def find_maximized_capital(k, w, profits, capital):
    n = len(profits)
    order = sorted(range(n), key=lambda i: capital[i])
    ready = []
    money = w
    nxt = 0
    for _ in range(k):
        while nxt < n and capital[order[nxt]] <= money:
            heapq.heappush(ready, -profits[order[nxt]])
            nxt += 1
        if not ready:
            break
        money += -heapq.heappop(ready)
    return money


# ---- test harness ---------------------------------------------------------

seed = 502


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show(name, k, w, profits, capital):
    got = find_maximized_capital(k, w, profits, capital)
    print(f"{name}: k={k} w={w} profits={fmt(profits)} capital={fmt(capital)} -> {got}")


def main():
    show("example 1", 2, 0, [1, 2, 3], [0, 1, 1])
    show("example 2", 3, 0, [1, 2, 3], [0, 1, 2])
    show("nothing affordable", 1, 0, [5], [1])
    show("k beyond n", 10, 1, [1, 2, 3], [1, 1, 1])
    show("the small one first", 2, 0, [1, 100], [0, 1])
    show("no profit", 3, 5, [0, 0, 0], [0, 1, 2])
    show("the largest numbers", 2, 1000000000, [10000, 10000], [1000000000, 1000000000])
    # 300 random cases: 1 to 20 projects of profit 0 to 20 needing 0 to
    # 40, k from 1 to 25 and w from 0 to 10.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 20
        k = 1 + next_random() % 25
        w = next_random() % 11
        profits = []
        capital = []
        for _ in range(n):
            profits.append(next_random() % 21)
            capital.append(next_random() % 41)
        got = find_maximized_capital(k, w, profits, capital)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} random cases: total capital {total}, checksum {checksum}")


main()
