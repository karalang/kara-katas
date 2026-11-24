# LeetCode #1323: Maximum 69 Number -- Python mirror of the ★ Kāra arm:
# the number written out, its first 6 turned to a 9, the place that gains
# the most, and the text read back as a number.


def maximum69_number(num):
    return int(str(num).replace("6", "9", 1))


def main():
    asks = [9669, 9996, 9999, 6, 9, 6666]
    print(" ".join(str(maximum69_number(n)) for n in asks))
    count = 0
    total = 0
    check = 0
    for digits in range(1, 5):
        for pattern in range(1 << digits):
            num = 0
            for k in range(digits):
                num = num * 10 + (9 if (pattern >> k) & 1 == 1 else 6)
            got = maximum69_number(num)
            count += 1
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"every one of the {count} numbers: answers total {total}, checksum {check}")


main()
