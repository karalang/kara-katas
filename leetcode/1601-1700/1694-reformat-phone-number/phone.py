# LeetCode #1694: Reformat Phone Number -- mirrors phone.kara, the ★ arm:
# the digits, then blocks of three while more than four are left.


def reformat_number(number):
    digits = "".join(c for c in number if c.isdigit())
    blocks = []
    at = 0
    while len(digits) - at > 4:
        blocks.append(digits[at:at + 3])
        at += 3
    if len(digits) - at == 4:
        blocks.append(digits[at:at + 2])
        blocks.append(digits[at + 2:])
    else:
        blocks.append(digits[at:])
    return "-".join(blocks)


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, seed):
    alphabet = "0123456789 -"
    dashes = 0
    check = 0
    for _ in range(count):
        length = seed.next() % (most - 1) + 2
        first = seed.next() % length
        second = (first + 1 + seed.next() % (length - 1)) % length
        number = []
        for i in range(length):
            pick = seed.next() % 10 if i == first or i == second else seed.next() % 12
            number.append(alphabet[pick])
        answer = reformat_number("".join(number))
        for b in answer.encode():
            if b == 45:
                dashes += 1
            check = (check * 31 + b) % 1000000007
    print(f"{count} numbers of up to {most} characters: {dashes} dashes, checksum {check}")


def main():
    print(reformat_number("1-23-45 6"))
    print(reformat_number("123 4-567"))
    print(reformat_number("123 4-5678"))
    print(reformat_number("12"))
    print(reformat_number("1234"))
    print(reformat_number("12345"))
    print(reformat_number("--1 2 3 - 4 5 6 7--"))
    seed = Seed(1694)
    batch(3000, 12, seed)
    batch(300, 100, seed)
    batch(10, 100000, seed)


main()
