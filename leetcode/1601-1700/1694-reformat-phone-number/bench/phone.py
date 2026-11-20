# LeetCode #1694: Reformat Phone Number -- the bench's Python mirror: the ★
# arm on 100000 random numbers of 100 characters, all drawn first, each
# answered 40 times.


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


seed = 1694


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, length = 100000, 40, 100
    alphabet = "0123456789 -"
    numbers = []
    for _ in range(count):
        number = []
        for i in range(length):
            pick = next_random() % 10 if i < 2 else next_random() % 12
            number.append(alphabet[pick])
        numbers.append("".join(number))
    total = 0
    check = 0
    for r in range(rounds):
        for number in numbers:
            answer = reformat_number(number).encode()
            total += len(answer)
            check = (check * 31 + len(answer) + answer[len(answer) // 2] + answer[-1] + r) % 1000000007
    print(f"{count} numbers of {length} characters, {rounds} rounds: {total} characters out, checksum {check}")


main()
