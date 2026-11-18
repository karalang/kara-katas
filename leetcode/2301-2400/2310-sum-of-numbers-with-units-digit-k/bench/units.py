# LeetCode #2310: Sum of Numbers With Units Digit K -- the bench, the ★
# arm in Python. The least count from 1 to 10 whose multiple of k fits
# within num and leaves a multiple of 10.


def minimum_numbers(num, k):
    if num == 0:
        return 0
    for n in range(1, 11):
        if n * k <= num and (num - n * k) % 10 == 0:
            return n
    return -1


def main():
    check = 0
    for p in range(300):
        for num in range(3001):
            for k in range(10):
                check = (check * 31 + minimum_numbers(num, k) + 1 + p) % 1000000007
    print(f"300 passes over 3001 sums and 10 digits: checksum {check}")


main()
