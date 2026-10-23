# LeetCode #869: Reordered Power of 2 -- Python mirror of the bench program
# (the ★ arm, digit counts).


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


def main():
    limit = 1000000
    count = 0
    check = 0
    for n in range(1, limit + 1):
        if reordered_power_of_2(n):
            count += 1
            check = (check * 31 + n) % 1000000007
    print(f"n from 1 to {limit}: {count} true, checksum {check}")


main()
