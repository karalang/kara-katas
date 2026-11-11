# LeetCode #1118: Number of Days in a Month -- the bench in Python, the ★
# arm over the same 10^6 months and 40 rounds.


def is_leap(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def number_of_days(year, month):
    if month == 2:
        return 29 if is_leap(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


seed = 1118


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    years = []
    months = []
    for _ in range(1000000):
        years.append(1583 + next_random() % 517)
        months.append(1 + next_random() % 12)
    total = check = last = 0
    for _ in range(40):
        for i in range(len(years)):
            d = number_of_days(years[i] + (last & 1), months[i])
            total += d
            if i % 64 == 0:
                check = (check * 31 + d) % 1000000007
            last = d
    print(f"40 rounds over 10^6 months: {total} days, checksum {check}")


main()
