# LeetCode #1507: Reformat Date -- the bench: 100000 dates built once,
# then each reformatted ten times by the ★ arm.
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


seed = 1507


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


dates = []
for _ in range(100000):
    year = 1900 + next_random() % 201
    month = next_random() % 12
    day = 1 + next_random() % days_in(month, year)
    dates.append(f"{day}{suffix(day)} {MONTHS[month]} {year}")
check = 0
for _ in range(10):
    for date in dates:
        for b in reformat_date(date).encode():
            check = (check * 31 + b + 1) % 1000000007
print(f"1000000 dates reformatted, 100000 built once: checksum {check}")
