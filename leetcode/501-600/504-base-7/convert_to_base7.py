# LeetCode #504: Base 7 -- Python mirror of the ★ arm (the digits by
# repeated division, read back to front); see convert_to_base7.kara.


def convert_to_base7(num):
    if num == 0:
        return "0"
    n = abs(num)
    digits = []
    while n > 0:
        digits.append(n % 7)
        n //= 7
    out = "-" if num < 0 else ""
    for d in reversed(digits):
        out += f"{d}"
    return out


# ---- test harness ---------------------------------------------------------

seed = 504


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rem(a, b):
    # Kāra's % truncates toward zero, as C's does; Python's floors.
    r = abs(a) % b
    return -r if a < 0 else r


def show(num):
    print(f'{num} -> "{convert_to_base7(num)}"')


def main():
    for num in [100, -7, 0, 6, 7, 48, 49, -1, 10000000, -10000000]:
        show(num)
    # 300 random numbers from -100 to 100 or from the whole range
    # -10^7 to 10^7, in turn.
    count = 300
    digits = 0
    negative = 0
    checksum = 0
    for c in range(count):
        if c % 2 == 0:
            num = next_random() % 201 - 100
        else:
            hi = next_random()
            num = (hi * 65536 + next_random()) % 20000001 - 10000000
        s = convert_to_base7(num)
        if num < 0:
            negative += 1
            digits += len(s) - 1
        else:
            digits += len(s)
        # Read as decimal, the base 7 digits name one number.
        read = int(s)
        checksum = (checksum * 31 + rem(read, 1000000007) + 1000000007) % 1000000007
    print(f"{count} random numbers: {digits} digits, {negative} negative, checksum {checksum}")


main()
