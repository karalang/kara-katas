"""LeetCode #1154: Day of the Year -- the Python mirror of day_of_year.kara.

The days before the month, from a table of running totals, plus the day of
the month, plus one from March on in a leap year."""


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


BEFORE = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def day_of_year(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    leap_day = 1 if month > 2 and is_leap(year) else 0
    return BEFORE[month - 1] + day + leap_day


# ---- test harness ---------------------------------------------------------


def show(date):
    print(f"{date}  ->  {day_of_year(date)}")


def days_in(year, month):
    if month == 2:
        return 29 if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) else 28
    return 31 - (month - 1) % 7 % 2


def main():
    for d in ["2019-01-09", "2019-02-10", "2003-03-01", "2004-03-01", "1900-01-01",
              "1900-02-28", "1900-03-01", "1900-12-31", "2000-02-29", "2000-03-01",
              "2000-12-31", "2016-02-29", "2019-12-31"]:
        show(d)
    dates = wrong = check = longest = 0
    for year in range(1900, 2020):
        count = 0
        for month in range(1, 13):
            for day in range(1, days_in(year, month) + 1):
                count += 1
                dates += 1
                got = day_of_year(f"{year}-{month:02}-{day:02}")
                if got != count:
                    wrong += 1
                check = (check * 31 + got) % 1000000007
        longest = max(longest, count)
    print(f"{dates} dates: {wrong} wrong, longest year {longest} days, checksum {check}")


if __name__ == "__main__":
    main()
