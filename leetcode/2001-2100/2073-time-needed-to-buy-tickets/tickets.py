# LeetCode #2073: Time Needed to Buy Tickets -- the Python mirror of
# tickets.kara (the ★ arm): each person ahead of k buys up to tickets[k],
# each behind up to tickets[k] - 1.


def time_required_to_buy(tickets, k):
    want = tickets[k]
    time = 0
    for i, t in enumerate(tickets):
        time += min(t, want) if i <= k else min(t, want - 1)
    return time


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [([2, 3, 2], 2), ([5, 1, 1, 1], 0), ([1], 0), ([100], 0), ([1, 1, 1, 1], 3), ([3, 3, 3], 1), ([84, 49, 5, 24, 70, 77, 87, 8], 3)]
    for tickets, k in examples:
        print(f"{show(tickets)}, k = {k} -> {time_required_to_buy(tickets, k)}")
    seed = [2073]
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random(seed) % 100 + 1
        top = [1, 10, 100][next_random(seed) % 3]
        tickets = [next_random(seed) % top + 1 for _ in range(n)]
        k = next_random(seed) % n
        a = time_required_to_buy(tickets, k)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 lines: sum {total}, checksum {check}")
    print(f"100 people of 100, the last -> {time_required_to_buy([100] * 100, 99)}")


main()
