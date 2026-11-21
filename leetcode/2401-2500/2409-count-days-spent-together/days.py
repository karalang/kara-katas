# LeetCode #2409: Count Days Spent Together -- the mirror of the ★ arm:
# each "MM-DD" turned into a day of the year, the shared stay from the
# later arrival to the earlier departure.

seed = 2409
LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
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


def date(n):
    month = 0
    while n >= LENGTHS[month]:
        n -= LENGTHS[month]
        month += 1
    return f"{month + 1:02}-{n + 1:02}"


def stay():
    a = next_random() % 365
    b = next_random() % 365
    return date(min(a, b)), date(max(a, b))


def main():
    print(count_days_together("08-15", "08-18", "08-16", "08-19"))
    print(count_days_together("10-01", "10-31", "11-01", "12-31"))
    print(count_days_together("01-01", "12-31", "01-01", "12-31"))
    print(count_days_together("02-28", "02-28", "02-28", "02-28"))
    print(count_days_together("03-01", "06-30", "01-15", "03-01"))
    first = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    print(" ".join(str(count_days_together("01-01", "12-31", date(first[m]), date(first[m + 1] - 1))) for m in range(12)))
    check = 0
    total = 0
    for _ in range(3000):
        arrive_alice, leave_alice = stay()
        arrive_bob, leave_bob = stay()
        a = count_days_together(arrive_alice, leave_alice, arrive_bob, leave_bob)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
