# LeetCode #2483: Minimum Penalty for a Shop -- bench, Python mirror of
# shop.kara.


def best_closing_time(customers):
    balance = 0
    best = 0
    best_hour = 0
    hour = 0
    for c in customers:
        if c == 'Y':
            balance += 1
        else:
            balance -= 1
        hour += 1
        if balance > best:
            best = balance
            best_hour = hour
    return best_hour


seed = 2483


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    logs = [['Y' if next_random() % 2 == 0 else 'N' for _ in range(10000)] for _ in range(20)]
    check = 0
    for p in range(600):
        for g in range(20):
            at = check % 10000
            logs[g][at] = 'N' if logs[g][at] == 'Y' else 'Y'
            log = "".join(logs[g])
            check = (check * 31 + best_closing_time(log) + p) % 1000000007
    print(f"600 passes over 20 logs of 10^4 hours: checksum {check}")


main()
