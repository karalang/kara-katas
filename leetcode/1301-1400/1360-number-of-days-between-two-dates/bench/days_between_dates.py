# LeetCode #1360 bench -- Python: each date as its count of days from
# 1971-01-01, the answer the two counts' distance.


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def days_from_1971(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    days = day - 1
    for y in range(1971, year):
        days += 366 if is_leap(y) else 365
    for m in range(1, month):
        days += LENGTHS[m - 1]
        if m == 2 and is_leap(year):
            days += 1
    return days


def days_between_dates(date1, date2):
    return abs(days_from_1971(date1) - days_from_1971(date2))


seed = 1360


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_date():
    year = 1971 + next_random() % 130
    month = 1 + next_random() % 12
    last = LENGTHS[month - 1]
    if month == 2 and is_leap(year):
        last += 1
    day = 1 + next_random() % last
    return f"{year}-{month:02}-{day:02}"


def main():
    # 1000 dates written once; then 3 * 10^5 questions, each pair of dates
    # drawn from the checksum so far, every answer folded into it
    dates = [random_date() for _ in range(1000)]
    check = 0
    for r in range(300000):
        a = check % 1000
        b = (check // 1000 + r) % 1000
        check = (check * 31 + days_between_dates(dates[a], dates[b]) + r) % 1000000007
    print(f"300000 questions: checksum {check}")


main()
