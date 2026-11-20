# LeetCode #1281: Subtract the Product and Sum of Digits of an Integer --
# Python mirror of the ★ arm: the digits by remainders.


def subtract_product_and_sum(n):
    product = 1
    total = 0
    rest = n
    while rest > 0:
        digit = rest % 10
        product *= digit
        total += digit
        rest //= 10
    return product - total


def main():
    print(f"{subtract_product_and_sum(234)} {subtract_product_and_sum(4421)} {subtract_product_and_sum(1)} {subtract_product_and_sum(99999)} {subtract_product_and_sum(100000)}")
    total = 0
    check = 0
    zero = 0
    for n in range(1, 100001):
        got = subtract_product_and_sum(n)
        total += got
        if got == 0:
            zero += 1
        check = (check * 131 + got + 1000) % 1000000007
    print(f"1 to 100000: total {total}, {zero} zero, checksum {check}")


main()
