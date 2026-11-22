# LeetCode #2844: Minimum Operations to Make a Special Number -- the
# bench, mirrored from special.kara: one pass from the right, ending
# the number at the first 0 or 5 after a 0, or 2 or 7 after a 5.

seed = 2844


def minimum_operations(num):
    n = len(num)
    zero = False
    five = False
    for i in range(n - 1, -1, -1):
        d = num[i]
        if (zero and (d == 48 or d == 53)) or (five and (d == 50 or d == 55)):
            return n - i - 2
        if d == 48:
            zero = True
        if d == 53:
            five = True
    return n - 1 if zero else n


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 100000, 300
    numbers = []
    for _ in range(count):
        n = next_random() % 100 + 1
        digits = bytearray()
        for i in range(n):
            low = 1 if i == 0 and n > 1 else 0
            digits.append(48 + low + next_random() % (10 - low))
        numbers.append(bytes(digits))
    total = 0
    check = 0
    for r in range(rounds):
        for num in numbers:
            ops = minimum_operations(num)
            total += ops
            check = (check * 31 + ops + r) % 1000000007
    print(f"{count} numbers, {rounds} rounds: {total} operations, checksum {check}")


main()
