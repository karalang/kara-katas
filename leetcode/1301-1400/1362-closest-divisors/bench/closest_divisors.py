# LeetCode #1362 bench -- Python: d counts down from the square root of
# num + 2, and the first d that divides num + 1 or num + 2 gives the answer.
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


def main():
    # 10^4 questions, each num up to 10^9 drawn from the checksum so far,
    # both parts of every answer folded into it
    check = 0
    for r in range(10000):
        num = 1 + (check * 7919 + r) % 1000000000
        pair = closest_divisors(num)
        check = (check * 31 + pair[0] * 7 + pair[1] + r) % 1000000007
    print(f"10000 questions: checksum {check}")


main()
