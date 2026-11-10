# LeetCode #2073: Time Needed to Buy Tickets -- Python mirror of the ★
# arm's benchmark (tickets.kara): 20000 lines of 100 people, every place
# in every line asked about, 2000000 answers.


def time_required_to_buy(tickets, k):
    want = tickets[k]
    time = 0
    for i, t in enumerate(tickets):
        time += min(t, want) if i <= k else min(t, want - 1)
    return time


def main():
    seed = 2073

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lines = []
    for _ in range(20000):
        lines.append([next_random() % 100 + 1 for _ in range(100)])
    total = 0
    check = 0
    for tickets in lines:
        for k in range(100):
            a = time_required_to_buy(tickets, k)
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"2000000 answers: sum {total}, checksum {check}")


main()
