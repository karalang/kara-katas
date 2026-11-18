# LeetCode #2303: Calculate Amount Paid in Taxes -- the bench, the ★ arm
# in Python. Walk the brackets in order, taxing the part of the income
# inside each at its percent, summed in hundredths and divided once at
# the end.

seed = 2303


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def calculate_tax(brackets, income):
    hundredths = 0
    below = 0
    for upper, percent in brackets:
        if below >= income:
            break
        hundredths += (min(upper, income) - below) * percent
        below = upper
    return hundredths / 100.0


def main():
    lists = []
    for _ in range(20):
        brackets = []
        for i in range(100):
            less = 0 if i == 99 else next_random() % 5
            brackets.append((10 * (i + 1) - less, next_random() % 101))
        lists.append(brackets)
    check = 0
    for _ in range(100):
        for brackets in lists:
            for income in range(1001):
                tax = round(calculate_tax(brackets, income) * 100.0)
                check = (check * 31 + tax) % 1000000007
    print(f"100 passes over 20 lists of 100 brackets and 1001 incomes: checksum {check}")


main()
