# LeetCode #2160: Minimum Sum of Four Digit Number After Splitting Digits
# -- the benchmark's Python mirror of digits.kara.


def minimum_sum(num):
    d = sorted(int(c) for c in str(num))
    return (d[0] * 10 + d[2]) + (d[1] * 10 + d[3])


def main():
    total = 0
    check = 0
    for p in range(200):
        for k in range(9000):
            num = 1000 + (k + 37 * p) % 9000
            s = minimum_sum(num)
            total += s
            check = (check * 31 + s + p) % 1000000007
    print(f"1800000 solves: {total} in all, checksum {check}")


main()
