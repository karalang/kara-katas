"""LeetCode #1154 bench -- mirrors day_of_year.kara: the same dates, the
same passes, the ★ arm's table."""

BEFORE = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_year(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    leap_day = 1 if month > 2 and is_leap(year) else 0
    return BEFORE[month - 1] + day + leap_day


def days_in(year, month):
    if month == 2:
        return 29 if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) else 28
    return 31 - (month - 1) % 7 % 2


def main():
    passes = 1000
    dates = []
    for year in range(1900, 2020):
        for month in range(1, 13):
            for day in range(1, days_in(year, month) + 1):
                dates.append(f"{year}-{month:02}-{day:02}")
    total = 0
    check = 0
    for p in range(passes):
        for date in dates:
            n = day_of_year(date)
            total += n
            check = (check * 31 + n + p) % 1000000007
    print(f"{passes} passes over {len(dates)} dates: total {total}, checksum {check}")


if __name__ == "__main__":
    main()
