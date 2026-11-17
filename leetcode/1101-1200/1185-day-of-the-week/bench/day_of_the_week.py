# LeetCode #1185: Day of the Week -- the ★ arm in Python: the days from
# 1 January 1971, a Friday, to the date, and that many days on from Friday.

NAMES = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def day_of_the_week(day, month, year):
    days = 0
    for y in range(1971, year):
        days += 366 if is_leap(y) else 365
    for m in range(1, month):
        days += MONTH_DAYS[m - 1]
    if month > 2 and is_leap(year):
        days += 1
    days += day - 1
    return NAMES[days % 7]


def main():
    seed = 1185

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    dates = []
    for _ in range(10000):
        year = 1971 + next_random() % 130
        month = 1 + next_random() % 12
        length = 29 if month == 2 and is_leap(year) else MONTH_DAYS[month - 1]
        day = 1 + next_random() % length
        dates.append((day, month, year))
    rounds = 100
    check = 0
    for r in range(rounds):
        for day, month, year in dates:
            name = day_of_the_week(day, month, year)
            check = (check * 131 + len(name) * 7 + ord(name[0]) + r) % 1000000007
    print(f"{rounds} rounds of 10000 dates: checksum {check}")


main()
