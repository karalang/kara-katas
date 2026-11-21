# LeetCode #2409: Count Days Spent Together -- the bench, the ★ arm in
# Python: each "MM-DD" read from its characters into a day of the year,
# the shared stay from the later arrival to the earlier departure.

seed = 2409
BEFORE = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def day_of_year(date):
    month = (ord(date[0]) - 48) * 10 + ord(date[1]) - 48
    day = (ord(date[3]) - 48) * 10 + ord(date[4]) - 48
    return BEFORE[month - 1] + day


def count_days_together(arrive_alice, leave_alice, arrive_bob, leave_bob):
    first = max(day_of_year(arrive_alice), day_of_year(arrive_bob))
    last = min(day_of_year(leave_alice), day_of_year(leave_bob))
    return max(last - first + 1, 0)


def main():
    lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    names = [f"{m + 1:02}-{d + 1:02}" for m in range(12) for d in range(lengths[m])]
    stays = []
    for _ in range(100000):
        a, b = next_random() % 365, next_random() % 365
        c, d = next_random() % 365, next_random() % 365
        stays.append((min(a, b), max(a, b), min(c, d), max(c, d)))
    check = 0
    for p in range(100):
        for a, b, c, d in stays:
            check = (check * 31 + count_days_together(names[a], names[b], names[c], names[d]) + p) % 1000000007
    print(f"100 passes over 10^5 pairs of stays: checksum {check}")


main()
