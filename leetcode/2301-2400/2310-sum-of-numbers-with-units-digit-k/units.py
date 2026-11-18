# LeetCode #2310: Sum of Numbers With Units Digit K -- the ★ arm in
# Python. The least n from 1 to 10 with n k <= num and num - n k a
# multiple of 10; 0 for a sum of 0, and -1 when no n fits.


def minimum_numbers(num, k):
    if num == 0:
        return 0
    for n in range(1, 11):
        if n * k <= num and (num - n * k) % 10 == 0:
            return n
    return -1


def main():
    cases = [(58, 9), (37, 2), (0, 7), (10, 0), (0, 0), (3000, 9), (2999, 1), (3000, 3), (2998, 5)]
    for num, k in cases:
        print(f"{num}, {k}: {minimum_numbers(num, k)}")
    check = 0
    impossible = 0
    for num in range(201):
        for k in range(10):
            size = minimum_numbers(num, k)
            check = (check * 31 + size + 1) % 1000000007
            if size < 0:
                impossible += 1
    print(f"2010 cases: checksum {check}, {impossible} impossible")


main()
