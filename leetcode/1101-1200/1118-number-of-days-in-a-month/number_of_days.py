# LeetCode #1118: Number of Days in a Month -- Python mirror of the ★ arm.


def is_leap(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def number_of_days(year, month):
    if month == 2:
        return 29 if is_leap(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def main():
    print(f"1992 7 -> {number_of_days(1992, 7)}")
    print(f"2000 2 -> {number_of_days(2000, 2)}")
    print(f"1900 2 -> {number_of_days(1900, 2)}")
    for year in [2023, 2024, 2100, 1583, 1600]:
        days = [str(number_of_days(year, m)) for m in range(1, 13)]
        print(f"{year}: {' '.join(days)}")
    total = leap = check = 0
    for year in range(1583, 2101):
        for month in range(1, 13):
            d = number_of_days(year, month)
            total += d
            if month == 2 and d == 29:
                leap += 1
            check = (check * 31 + d) % 1000000007
    print(f"1583 to 2100: {total} days, {leap} leap years, checksum {check}")


main()
