# LeetCode #1012: Numbers With Repeated Digits -- counting arrangements.
# Mirrors num_dup_digits.kara line for line.


def num_dup_digits_at_most_n(n):
    return n - distinct_up_to(n)


def distinct_up_to(n):
    digits = []
    rest = n
    while rest > 0:
        digits.append(rest % 10)
        rest //= 10
    digits.reverse()
    length = len(digits)
    count = 0
    for k in range(1, length):
        count += 9 * arrangements(9, k - 1)
    seen = [False] * 10
    for i in range(length):
        d = digits[i]
        lowest = 1 if i == 0 else 0
        for smaller in range(lowest, d):
            if not seen[smaller]:
                count += arrangements(9 - i, length - i - 1)
        if seen[d]:
            return count
        seen[d] = True
    return count + 1


def arrangements(free, slots):
    ways = 1
    for j in range(slots):
        ways *= free - j
    return ways


seed = 1012


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = [20, 100, 1000, 1, 10, 11, 99, 101, 110, 1022, 98765, 123456789, 987654321, 999999999, 1000000000]
    for n in examples:
        print(f"n = {n} -> {num_dup_digits_at_most_n(n)}")
    below = []
    power = 10
    for _ in range(9):
        below.append(str(num_dup_digits_at_most_n(power - 1)))
        power *= 10
    shown = ",".join(below)
    print(f"10^k - 1 for k = 1..9 -> [{shown}]")
    total = 0
    check = 0
    for n in range(1, 5001):
        count = num_dup_digits_at_most_n(n)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"every n up to 5000: counts sum to {total}, checksum {check}")
    for draws, top in [(1000, 1000), (1000, 1000000), (200, 1000000000)]:
        total = 0
        check = 0
        for _ in range(draws):
            n = 1 + (next_random() * 32768 + next_random()) % top
            count = num_dup_digits_at_most_n(n)
            total += count
            check = (check * 31 + count) % 1000000007
        print(f"{draws} random n up to {top}: counts sum to {total}, checksum {check}")


main()
