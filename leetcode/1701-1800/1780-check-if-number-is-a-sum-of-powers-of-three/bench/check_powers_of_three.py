# LeetCode #1780: Check if Number is a Sum of Powers of Three -- the bench in
# Python, mirroring check_powers_of_three.kara: base-3 digits read off from
# the lowest, on every n from 1 to 10^7, five rounds over.


def check_powers_of_three(n):
    rest = n
    while rest > 0:
        if rest % 3 == 2:
            return False
        rest //= 3
    return True


def main():
    count = 0
    check = 0
    for round in range(5):
        for n in range(1, 10000001):
            if check_powers_of_three(n):
                count += 1
                check = (check * 31 + n + round) % 1000000007
    print(f"5 rounds of 1 to 10000000: {count} sums, checksum {check}")


main()
