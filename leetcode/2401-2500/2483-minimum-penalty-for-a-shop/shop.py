# LeetCode #2483: Minimum Penalty for a Shop -- Python mirror of
# shop.kara: by a running balance.


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


def random_log(n, yes):
    return "".join("Y" if next_random() % 100 < yes else "N" for _ in range(n))


def main():
    for log in ["YYNY", "NNNNN", "YYYY", "Y", "N", "YN", "NY", "YNYN"]:
        print(f"{log} -> {best_closing_time(log)}")
    print(f"10^5 Y -> {best_closing_time('Y' * 100000)}")
    print(f"10^5 N -> {best_closing_time('N' * 100000)}")
    print(f"\"YN\" x 50000 -> {best_closing_time('YN' * 50000)}")
    for yes in [50, 60]:
        log = random_log(100000, yes)
        print(f"10^5 random at {yes} in 100 -> {best_closing_time(log)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        yes = next_random() % 101
        check = (check * 31 + best_closing_time(random_log(n, yes))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
