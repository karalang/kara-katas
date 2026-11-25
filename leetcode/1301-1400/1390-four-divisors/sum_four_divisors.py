# LeetCode #1390: Four Divisors -- Python mirror of the ★ arm: trial
# division up to the square root, divisors taken in pairs, the search
# given up once past four.


def sum_four_divisors(nums):
    total = 0
    for v in nums:
        count = 0
        s = 0
        d = 1
        while d * d <= v and count <= 4:
            if v % d == 0:
                count += 1
                s += d
                if d * d != v:
                    count += 1
                    s += v // d
            d += 1
        if count == 4:
            total += s
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    shown = [
        sum_four_divisors([21, 4, 7]),
        sum_four_divisors([21, 21]),
        sum_four_divisors([1, 2, 3, 4, 5]),
        sum_four_divisors([8, 27]),
        sum_four_divisors([49]),
        sum_four_divisors([100000]),
    ]
    print(" ".join(str(x) for x in shown))
    seed = 1390
    wide = []
    for _ in range(10000):
        a = next_random()
        b = next_random()
        wide.append(1 + (a * 32768 + b) % 100000)
    top = list(range(90001, 100001))
    print(f"10^4 values: {sum_four_divisors(wide)}, and {sum_four_divisors(top)} for 90001 to 10^5")
    check = 0
    total = 0
    for c in range(2000):
        n = 1 + next_random() % 50
        most = 100000 if c % 2 == 0 else 100
        nums = [1 + next_random() % most for _ in range(n)]
        got = sum_four_divisors(nums)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random lists: {total} in all, checksum {check}")


main()
