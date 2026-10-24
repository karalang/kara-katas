# LeetCode #983: Minimum Cost For Tickets -- mirror of the ★ arm
# (mincost_tickets.kara), a table over the calendar.


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


# ---- test harness ---------------------------------------------------------

seed = 983


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(days, costs):
    shown = f"{days[0]} to {days[-1]} ({len(days)} days)" if len(days) > 12 else fmt(days)
    print(f"days {shown}, costs {fmt(costs)} -> {mincost_tickets(days, costs)}")


def random_days(n, span):
    days = []
    need = n
    for d in range(1, span + 1):
        if need > 0 and next_random() % (span - d + 1) < need:
            days.append(d)
            need -= 1
    return days


def main():
    show([1, 4, 6, 7, 8, 20], [2, 7, 15])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])
    show([1], [2, 7, 15])
    show([365], [9, 4, 20])
    show([1, 3, 5], [7, 2, 15])
    show([1, 2, 3, 4, 5], [2, 7, 1])
    show([1, 8, 15, 22], [3, 3, 9])
    show([1, 31, 61], [20, 30, 5])
    year = list(range(1, 366))
    show(year, [2, 7, 15])
    show(year, [1000, 1000, 1])
    for count, most, span, top in [(300, 12, 40, 20), (3000, 60, 365, 100), (4, 365, 365, 1000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = 1 + next_random() % most
            days = random_days(n, span)
            costs = [1 + next_random() % top, 1 + next_random() % top, 1 + next_random() % top]
            c = mincost_tickets(days, costs)
            total += c
            check = (check * 31 + c) % 1000000007
        print(f"{count} random plans of up to {most} days within {span}: cost {total}, checksum {check}")


main()
