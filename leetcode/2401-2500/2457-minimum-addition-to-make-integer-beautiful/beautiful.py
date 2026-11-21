# LeetCode #2457: Minimum Addition to Make Integer Beautiful -- Python
# mirror of beautiful.kara: while the digit sum is too large, n + x is
# rounded up to the next multiple of a power of ten one place higher.


def digit_sum(x):
    rest = x
    total = 0
    while rest > 0:
        total += rest % 10
        rest //= 10
    return total


def make_integer_beautiful(n, target):
    m = n
    p = 1
    while digit_sum(m) > target:
        p *= 10
        m = (m + p - 1) // p * p
    return m - n


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(make_integer_beautiful(16, 6))
    print(make_integer_beautiful(467, 6))
    print(make_integer_beautiful(1, 1))
    print(make_integer_beautiful(1000000000000, 1))
    print(make_integer_beautiful(999999999999, 1))
    print(make_integer_beautiful(19, 1))
    print(make_integer_beautiful(190, 1))
    print(make_integer_beautiful(999999999999, 108))
    seed = 2457
    check = 0
    total = 0
    for _ in range(2000):
        a = next_random()
        b = next_random()
        n = 1 + (a * 1073741824 + b * 32768 + next_random()) % 1000000000000
        target = 1 + next_random() % 150
        answer = make_integer_beautiful(n, target)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"2000 values up to 10^12: checksum {check}, total {total}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 10000
        target = 1 + next_random() % 20
        check = (check * 31 + make_integer_beautiful(n, target)) % 1000000007
    print(f"3000 random: checksum {check}")


main()
