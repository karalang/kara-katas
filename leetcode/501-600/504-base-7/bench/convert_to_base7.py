# Benchmark for #504 in Python: the ★ arm (the digits by repeated
# division); see ../convert_to_base7.kara.


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


def rem(a, b):
    # Kāra's % truncates toward zero, as C's does; Python's floors.
    r = abs(a) % b
    return -r if a < 0 else r


def main():
    # 5,000,001 numbers across the whole range, -10^7 to 10^7 in steps
    # of 4. Each string is read back as a decimal number, which the base
    # 7 digits name uniquely, and folded into a checksum.
    count = 5000001
    digits = 0
    checksum = 0
    for i in range(count):
        num = -10000000 + 4 * i
        s = convert_to_base7(num)
        digits += len(s)
        read = int(s)
        checksum = (checksum * 31 + rem(read, 1000000007) + 1000000007) % 1000000007
    print(f"{count} numbers: {digits} characters, checksum {checksum}")


main()
