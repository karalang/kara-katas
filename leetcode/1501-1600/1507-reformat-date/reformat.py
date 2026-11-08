# LeetCode #1507: Reformat Date -- the Python mirror of the ★ arm: split
# on spaces, the day's leading digits, the month's place in the table, and
# the year as it is.
import itertools

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def reformat_date(date):
    parts = date.split(" ")
    day = int("".join(itertools.takewhile(str.isdigit, parts[0])))
    month = MONTHS.index(parts[1]) + 1
    return f"{parts[2]}-{month:02}-{day:02}"


def suffix(day):
    if day in (1, 21, 31):
        return "st"
    if day in (2, 22):
        return "nd"
    if day in (3, 23):
        return "rd"
    return "th"


def days_in(month, year):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return 29 if month == 1 and leap else days[month]


def write_date(day, month, year):
    return f"{day}{suffix(day)} {MONTHS[month]} {year}"


seed = 1507


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def fold(check, out):
    for b in out.encode():
        check = mix(check, b)
    return check


examples = ["20th Oct 2052", "6th Jun 1933", "26th May 1960", "1st Jan 1900", "31st Dec 2100", "22nd Feb 2000", "3rd Mar 2003", "29th Feb 2096"]
for date in examples:
    print(f"{date} -> {reformat_date(date)}")
check = 0
count = 0
for year in [1900, 1901, 2000, 2052, 2100]:
    for month in range(12):
        for day in range(1, days_in(month, year) + 1):
            check = fold(check, reformat_date(write_date(day, month, year)))
            count += 1
print(f"{count} dates, every day of five years: checksum {check}")
check = 0
for _ in range(3000):
    year = 1900 + next_random() % 201
    month = next_random() % 12
    day = 1 + next_random() % days_in(month, year)
    check = fold(check, reformat_date(write_date(day, month, year)))
print(f"3000 random dates from 1900 to 2100: checksum {check}")
