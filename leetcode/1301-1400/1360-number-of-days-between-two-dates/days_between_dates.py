# LeetCode #1360 -- Python mirror of the ★ arm: each date as its count of
# days from 1971-01-01, the years and months before it added up.


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def days_from_1971(date):
    year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
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


seed = [1360]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_date():
    year = 1971 + next_random() % 130
    month = 1 + next_random() % 12
    last = LENGTHS[month - 1]
    if month == 2 and is_leap(year):
        last += 1
    day = 1 + next_random() % last
    return f"{year}-{month:02}-{day:02}"


def main():
    e1 = days_between_dates("2019-06-29", "2019-06-30")
    e2 = days_between_dates("2020-01-15", "2019-12-31")
    same = days_between_dates("1999-12-31", "1999-12-31")
    ends = days_between_dates("2100-12-31", "1971-01-01")
    leap = days_between_dates("2000-02-28", "2000-03-01")
    plain = days_between_dates("2100-02-28", "2100-03-01")
    print(f"{e1} {e2} {same} {ends} {leap} {plain}")
    total = 0
    check = 0
    for _ in range(2000):
        a = random_date()
        b = random_date()
        got = days_between_dates(a, b)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random pairs: {total} days in all, checksum {check}")


main()
