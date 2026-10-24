# Benchmark: LeetCode #983 Minimum Cost For Tickets -- the ★ arm, a
# table over the calendar, on plans of up to LeetCode's 365 days.
# Mirrors mincost_tickets.kara, .rs, .c and go-seq/.


def mincost_tickets(days, costs):
    last = days[-1]
    travel = [False] * (last + 1)
    for d in days:
        travel[d] = True
    best = [0] * (last + 1)
    for d in range(1, last + 1):
        if not travel[d]:
            best[d] = best[d - 1]
            continue
        week = best[d - 7] if d >= 7 else 0
        month = best[d - 30] if d >= 30 else 0
        best[d] = min(best[d - 1] + costs[0], week + costs[1], month + costs[2])
    return best[last]


seed = 983


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 300
    plans = []
    prices = []
    for _ in range(1000):
        n = 1 + next_random() % 365
        days = []
        need = n
        for d in range(1, 366):
            if need > 0 and next_random() % (366 - d) < need:
                days.append(d)
                need -= 1
        plans.append(days)
        prices.append([1 + next_random() % 1000, 1 + next_random() % 1000, 1 + next_random() % 1000])
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(1000):
            j = (r + i) % 1000
            c = mincost_tickets(plans[j], prices[j])
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"{rounds} rounds over 1000 plans of up to 365 days: cost {total}, checksum {check}")


main()
