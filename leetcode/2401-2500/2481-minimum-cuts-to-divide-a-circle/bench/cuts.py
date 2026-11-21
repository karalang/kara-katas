# LeetCode #2481: Minimum Cuts to Divide a Circle -- bench, Python mirror
# of cuts.kara.


def number_of_cuts(n):
    if n == 1:
        return 0
    elif n % 2 == 0:
        return n // 2
    else:
        return n


def main():
    check = 0
    for p in range(500000):
        start = check % 100
        for i in range(100):
            n = 1 + (start + i) % 100
            check = (check * 31 + number_of_cuts(n) + p) % 1000000007
    print(f"500000 passes over every count from 1 to 100: checksum {check}")


main()
