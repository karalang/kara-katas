# LeetCode #2520: Count the Digits That Divide a Number -- benchmark mirror
# of the ★ arm (digits.kara): 100000 numbers built once, then the passes,
# each asking every number from an offset the checksum picks.


def count_digits(num):
    rest = num
    count = 0
    while rest > 0:
        if num % (rest % 10) == 0:
            count += 1
        rest //= 10
    return count


seed = 2520


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    nums = []
    for _ in range(100000):
        length = next_random() % 9 + 1
        num = 0
        for _ in range(length):
            num = num * 10 + next_random() % 9 + 1
        nums.append(num)
    passes = 150
    check = 0
    for p in range(passes):
        start = check % 100000
        for i in range(100000):
            check = (check * 31 + count_digits(nums[(start + i) % 100000]) + p) % 1000000007
    print(f"{passes} passes over 100000 numbers: checksum {check}")


main()
