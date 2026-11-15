# LeetCode #2180: Count Integers With Even Digit Sum -- the Python mirror
# of even_digits.kara: every number from 1 to num, its digit sum by
# remainders.


def count_even(num):
    count = 0
    for x in range(1, num + 1):
        total = 0
        rest = x
        while rest > 0:
            total += rest % 10
            rest //= 10
        if total % 2 == 0:
            count += 1
    return count


# ---- test harness ---------------------------------------------------------


def show(num):
    print(f"{num} -> {count_even(num)}")


def main():
    for num in [4, 30, 1, 2, 11, 1000]:
        show(num)
    total = 0
    check = 0
    for num in range(1, 1001):
        found = count_even(num)
        total += found
        check = (check * 31 + found) % 1000000007
    print(f"every number from 1 to 1000: {total} in all, checksum {check}")


main()
