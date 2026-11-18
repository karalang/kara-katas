# LeetCode #2303: Calculate Amount Paid in Taxes -- mirror of the ★ arm
# (tax.kara): the brackets walked in order, the tax summed in exact
# hundredths of a dollar and divided once at the end.


def calculate_tax(brackets, income):
    hundredths = 0
    below = 0
    for upper, percent in brackets:
        if below >= income:
            break
        hundredths += (min(upper, income) - below) * percent
        below = upper
    return hundredths / 100.0


# ---- test harness ----------------------------------------------------------

seed = 2303


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([(3, 50), (7, 10), (12, 25)], 10),
        ([(1, 0), (4, 25), (5, 50)], 2),
        ([(2, 50)], 0),
        ([(5, 10), (9, 20)], 5),
        ([(1, 0), (2, 100), (10, 33)], 10),
        ([(1000, 100)], 1000),
    ]
    for brackets, income in cases:
        print(f"{income}: {calculate_tax(brackets, income):.5f}")
    check = 0
    cents = 0
    for _ in range(2000):
        brackets = []
        upper = 0
        for _ in range(next_random() % 10 + 1):
            if upper < 1000:
                upper = min(upper + next_random() % 150 + 1, 1000)
                brackets.append((upper, next_random() % 101))
        income = next_random() % (upper + 1)
        tax = round(calculate_tax(brackets, income) * 100.0)
        check = (check * 31 + tax) % 1000000007
        cents += tax
    print(f"2000 cases: checksum {check}, {cents} cents in all")


main()
