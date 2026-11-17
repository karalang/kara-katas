# LeetCode #2235: Add Two Integers -- the benchmark's Python mirror of
# add.kara: 10^7 pairs drawn and added, folded into a checksum.


def sum_of(num1, num2):
    return num1 + num2


seed = 2235


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(10000000):
        num1 = next_random() % 201 - 100
        num2 = next_random() % 201 - 100
        check = (check * 31 + sum_of(num1, num2) + 200) % 1000000007
    print(f"10^7 pairs: checksum {check}")


main()
