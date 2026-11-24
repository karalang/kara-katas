# LeetCode #1323 bench, Python mirror of the Kāra bench: the ★ arm (the
# number written out, its first 6 turned to a 9, and the text read back) on
# the 30 numbers the constraints allow; 100000 passes over all 30, each
# pass starting at a place chosen by the checksum so far and folding every
# answer plus the pass into it.


def maximum69_number(num):
    return int(str(num).replace("6", "9", 1))


def main():
    nums = []
    for digits in range(1, 5):
        for pattern in range(1 << digits):
            num = 0
            for k in range(digits):
                num = num * 10 + (9 if (pattern >> k) & 1 == 1 else 6)
            nums.append(num)
    check = 0
    for p in range(100000):
        start = check % 30
        for k in range(30):
            got = maximum69_number(nums[(start + k) % 30])
            check = (check * 31 + got + p) % 1000000007
    print(f"100000 passes over the 30 numbers: checksum {check}")


main()
