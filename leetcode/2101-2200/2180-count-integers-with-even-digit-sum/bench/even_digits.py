# LeetCode #2180: Count Integers With Even Digit Sum -- the benchmark's
# Python mirror of even_digits.kara.


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


seed = 2180


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(200000):
        num = next_random() % 1000 + 1
        check = (check * 31 + count_even(num)) % 1000000007
    print(f"200000 solves: checksum {check}")


main()
