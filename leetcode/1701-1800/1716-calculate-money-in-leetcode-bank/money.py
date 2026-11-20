# LeetCode #1716: Calculate Money in Leetcode Bank -- the Python mirror of
# the ★ arm (money.kara): whole weeks and the days left, each summed in
# closed form.


def total_money(n):
    weeks, days = n // 7, n % 7
    return 28 * weeks + 7 * weeks * (weeks - 1) // 2 + days * (weeks + 1) + days * (days - 1) // 2


def main():
    # LeetCode's three examples, then one day, one week, and the last day
    print(total_money(4))
    print(total_money(10))
    print(total_money(20))
    print(total_money(1))
    print(total_money(7))
    print(total_money(1000))
    # every n the constraints allow
    total = 0
    check = 0
    for n in range(1, 1001):
        answer = total_money(n)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"every n from 1 to 1000: answers sum to {total}, checksum {check}")


main()
