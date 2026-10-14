# LeetCode #639: Decode Ways II -- Python mirror of the ★ arm.
#
# The count of decodings of every prefix, two at a time, modulo 10^9 + 7.

M = 1000000007


def alone(c):
    if c == "*":
        return 9
    if c == "0":
        return 0
    return 1


def together(a, b):
    if a == "*":
        if b == "*":
            return 15
        return 2 if b <= "6" else 1
    if a == "1":
        return 9 if b == "*" else 1
    if a == "2":
        if b == "*":
            return 6
        return 1 if b <= "6" else 0
    return 0


def num_decodings(s):
    before = 1
    last = alone(s[0])
    for i in range(1, len(s)):
        nxt = (last * alone(s[i]) + before * together(s[i - 1], s[i])) % M
        before = last
        last = nxt
    return last


seed = 639


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, stars, zeros):
    out = []
    for _ in range(n):
        if next_random() % 100 < stars:
            out.append("*")
        elif next_random() % 100 < zeros:
            out.append("0")
        else:
            out.append(str(1 + next_random() % 9))
    return "".join(out)


def ask(s):
    print(f"{s} -> {num_decodings(s)}")


def main():
    for s in ["*", "1*", "2*", "0", "10", "20", "30", "*0", "0*", "**", "*7",
              "27", "26", "*0*", "1*1*1*0"]:
        ask(s)
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        stars = next_random() % 60
        zeros = next_random() % 20
        count = num_decodings(random_text(n, stars, zeros))
        total = (total + count) % M
        checksum = (checksum * 31 + count) % M
    print(f"300 random strings: total {total}, checksum {checksum}")
    print(f"100000 stars -> {num_decodings('*' * 100000)}")
    mixed = random_text(100000, 30, 0)
    print(f"100000 mixed characters -> {num_decodings(mixed)}")


main()
