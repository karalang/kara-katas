# LeetCode #1012 bench: the ★ arm (counting arrangements) over 100,000
# values of n up to a billion, drawn once; each of 40 rounds counts every
# value shifted by its own amount and folds each count into a checksum.


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
    count = 100000
    rounds = 40
    values = [(next_random() * 32768 + next_random()) % 1000000000 for _ in range(count)]
    check = 0
    for r in range(rounds):
        for k in range(count):
            n = (values[k] + r * 7919) % 1000000000 + 1
            check = (check * 31 + num_dup_digits_at_most_n(n)) % 1000000007
    print(f"{rounds} rounds over {count} values of n: checksum {check}")


main()
