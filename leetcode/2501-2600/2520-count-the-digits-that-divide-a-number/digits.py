# LeetCode #2520: Count the Digits That Divide a Number -- Python mirror of
# the ★ arm (digits.kara): the digits peeled off by % 10 and // 10, each
# counted when it divides the number; and its harness, line for line.


def count_digits(num):
    rest = num
    count = 0
    while rest > 0:
        if num % (rest % 10) == 0:
            count += 1
        rest //= 10
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def no_zeros(length):
    num = 0
    for _ in range(length):
        num = num * 10 + next_random() % 9 + 1
    return num


def main():
    global seed
    for num in [7, 121, 1248, 1, 13, 111111111, 999999999, 987654321, 864]:
        print(f"{num} -> {count_digits(num)}")
    seed = 2520
    for most in [4, 9]:
        total = 0
        check = 0
        for _ in range(2000):
            a = count_digits(no_zeros(next_random() % most + 1))
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"2000 random of up to {most} digits: total {total}, checksum {check}")
    count, every, total = 0, 0, 0
    for num in range(1, 200001):
        if "0" not in str(num):
            a = count_digits(num)
            count += 1
            total += a
            if a == len(str(num)):
                every += 1
    print(f"1 to 2 10^5: {count} with no 0, {every} divided by every digit, total {total}")


main()
