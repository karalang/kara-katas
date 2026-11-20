# LeetCode #1702: Maximum Binary String After Change -- the bench's Python
# mirror: the ★ arm on 50 random strings of 100000 digits, all drawn
# first, each answered 40 times.


def maximum_binary_string(binary):
    # one 0 left, at the first 0 plus the zeros less one
    first = -1
    zeros = 0
    for i, b in enumerate(binary):
        if b == "0":
            if first < 0:
                first = i
            zeros += 1
    if zeros == 0:
        return binary
    out = []
    for i in range(len(binary)):
        out.append("0" if i == first + zeros - 1 else "1")
    return "".join(out)


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count, rounds, n = 50, 40, 100000
    seed = [1702]
    strings = []
    for _ in range(count):
        # each digit a 1 with a chance of its string's own, 0 to 10 in 10
        lean = next_random(seed) % 11
        strings.append("".join("1" if next_random(seed) % 10 < lean else "0" for _ in range(n)))
    ones = 0
    check = 0
    for _ in range(rounds):
        for binary in strings:
            answer = maximum_binary_string(binary)
            digits = answer.encode()
            # the 0's place, or the length when none is left
            zero = digits.find(b"0")
            if zero < 0:
                zero = len(digits)
            ones += len(digits) - (1 if zero < len(digits) else 0)
            check = (check * 31 + digits[check % len(digits)] + zero) % 1000000007
    print(f"{count} strings of {n} digits, {rounds} rounds: {ones} ones, checksum {check}")


main()
