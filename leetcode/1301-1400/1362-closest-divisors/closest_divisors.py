# LeetCode #1362: Closest Divisors -- Python mirror of the ★ arm: d counts
# down from the square root of num + 2, and the first d that divides
# num + 1 or num + 2 gives the answer.
import math


def isqrt(x):
    r = int(math.sqrt(x))
    while r * r > x:
        r -= 1
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r


def closest_divisors(num):
    one, two = num + 1, num + 2
    d = isqrt(two)
    while d > 0:
        if one % d == 0:
            return [d, one // d]
        if two % d == 0:
            return [d, two // d]
        d -= 1
    return [1, num + 1]


seed = 1362


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(pair):
    return f"[{min(pair)},{max(pair)}]"


def main():
    nums = [8, 123, 999, 1, 1000000000, 23, 1000000005]
    print(" ".join(show(closest_divisors(num)) for num in nums))
    check = 0
    for _ in range(500):
        a = next_random()
        b = next_random()
        num = 1 + (a * 32768 + b) % 1000000000
        pair = closest_divisors(num)
        check = (check * 131 + min(pair) * 7 + max(pair)) % 1000000007
    print(f"500 random numbers: checksum {check}")


main()
