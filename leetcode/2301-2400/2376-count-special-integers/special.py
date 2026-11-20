# LeetCode #2376: Count Special Integers -- Python mirror of the ★ arm,
# digit by digit.


def arrangements(free, places):
    ways = 1
    for k in range(places):
        ways *= free - k
    return ways


def count_special_numbers(n):
    digits = [int(c) for c in str(n)]
    length = len(digits)
    count = 0
    for l in range(1, length):
        count += 9 * arrangements(9, l - 1)
    used = [False] * 10
    for i in range(length):
        low = 1 if i == 0 else 0
        for d in range(low, digits[i]):
            if not used[d]:
                count += arrangements(9 - i, length - 1 - i)
        if used[digits[i]]:
            return count
        used[digits[i]] = True
    return count + 1


seed = 2376


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{count_special_numbers(20)} {count_special_numbers(5)} {count_special_numbers(135)}")
    print(f"{count_special_numbers(1)} {count_special_numbers(10)}")
    print(f"{count_special_numbers(2000000000)} {count_special_numbers(123456789)}")
    check = 0
    special = 0
    for _ in range(2000):
        digits = 1 + next_random() % 5
        top = 10 ** digits
        n = 1 + next_random() % (top - 1)
        t = count_special_numbers(n)
        check = (check * 31 + t) % 1000000007
        if t > count_special_numbers(n - 1) or n == 1:
            special += 1
    print(f"2000 values: checksum {check}, {special} special themselves")


main()
