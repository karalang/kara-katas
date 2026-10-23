# LeetCode #869: Reordered Power of 2 -- Python mirror of the ★ arm (digit
# counts).


def digit_counts(x):
    counts = [0] * 10
    rest = x
    while rest > 0:
        counts[rest % 10] += 1
        rest //= 10
    return counts


def reordered_power_of_2(n):
    want = digit_counts(n)
    power = 1
    for _ in range(30):
        if digit_counts(power) == want:
            return True
        power *= 2
    return False


seed = 869


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_n():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 1000000000 + 1


def shuffled(x):
    digits = list(str(x))
    n = len(digits)
    while True:
        for i in range(1, n):
            j = next_random() % (i + 1)
            digits[i], digits[j] = digits[j], digits[i]
        if digits[0] != "0":
            break
    return int("".join(digits))


def show(n):
    print(f"n = {n} -> {'true' if reordered_power_of_2(n) else 'false'}")


def main():
    show(1)
    show(10)
    for n in [16, 61, 46, 64, 128, 821, 218, 24, 125, 1024, 2014, 4021, 536870912, 102356789, 1000000000, 999999999]:
        show(n)
    count = 0
    check = 0
    for n in range(1, 100001):
        if reordered_power_of_2(n):
            count += 1
            check = (check * 31 + n) % 1000000007
    print(f"n from 1 to 100000: {count} true, checksum {check}")
    count = 0
    for _ in range(20000):
        if reordered_power_of_2(random_n()):
            count += 1
    print(f"20000 random n up to 10^9: {count} true")
    count = 0
    check = 0
    power = 1
    for _ in range(30):
        for _ in range(20):
            n = shuffled(power)
            if reordered_power_of_2(n):
                count += 1
            check = (check * 31 + n) % 1000000007
        power *= 2
    print(f"600 shuffled powers of two: {count} true, checksum {check}")


main()
