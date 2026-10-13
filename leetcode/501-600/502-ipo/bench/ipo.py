# Benchmark for #502: Python mirror of the ★ arm (projects sorted by
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


seed = 502


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 60 cases of 100,000 projects with k = 100,000, profits 0 to 10,000
    # and capital needs from 0 to 10^5, 10^7 or 10^9 in turn, w from 0
    # to 1,000; built once. Then each case is solved once.
    cases = 60
    n = 100000
    all_profits = []
    all_capital = []
    starts = []
    for c in range(cases):
        scale = 100001 if c % 3 == 0 else 10000001 if c % 3 == 1 else 1000000001
        profits = []
        capital = []
        for _ in range(n):
            profits.append(next_random() % 10001)
            hi = next_random()
            lo = next_random()
            capital.append((hi * 32768 + lo) % scale)
        all_profits.append(profits)
        all_capital.append(capital)
        starts.append(next_random() % 1001)
    total = 0
    checksum = 0
    for c in range(cases):
        got = find_maximized_capital(n, starts[c], all_profits[c], all_capital[c])
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{cases} cases of {n} projects: total capital {total}, checksum {checksum}")


main()
