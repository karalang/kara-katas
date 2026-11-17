# LeetCode #1185: Day of the Week -- the ★ arm in Python: the days from
# 1 January 1971, a Friday, to the date. Also checks every answer against
# Python's own calendar (`datetime.date.weekday`).
import datetime

NAMES = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
CALENDAR = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def day_of_the_week(day, month, year):
    days = sum(366 if is_leap(y) else 365 for y in range(1971, year))
    days += sum(MONTH_DAYS[: month - 1])
    if month > 2 and is_leap(year):
        days += 1
    days += day - 1
    return NAMES[days % 7]


def checked(day, month, year):
    got = day_of_the_week(day, month, year)
    assert got == CALENDAR[datetime.date(year, month, day).weekday()], (day, month, year)
    return got


print(f"example 1: {checked(31, 8, 2019)}")
print(f"example 2: {checked(18, 7, 1999)}")
print(f"example 3: {checked(15, 8, 1993)}")
print(f"first day: {checked(1, 1, 1971)}")
print(f"last day: {checked(31, 12, 2100)}")
print(f"leap day 2000: {checked(29, 2, 2000)}")
print(f"after 28 February 2100: {checked(1, 3, 2100)}")
print(f"leap day 1972: {checked(29, 2, 1972)}")
seed = 1185


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


checksum = 0
for t in range(3000):
    year = 1971 + next_random() % 130
    month = 1 + next_random() % 12
    length = 29 if month == 2 and is_leap(year) else MONTH_DAYS[month - 1]
    day = 1 + next_random() % length
    name = checked(day, month, year)
    checksum = (checksum * 31 + len(name) * 7 + ord(name[0]) + t) % 1000000007
print(f"3000 random dates: checksum {checksum}")
# every date in the range against the calendar
d = datetime.date(1971, 1, 1)
while d.year <= 2100:
    checked(d.day, d.month, d.year)
    d += datetime.timedelta(days=1)
