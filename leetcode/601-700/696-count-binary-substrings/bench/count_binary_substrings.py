# LeetCode #696: Count Binary Substrings -- bench program, Python mirror of the ★ arm.

seed = 696


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_binary_substrings(s):
    before, current, count = 0, 1, 0
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            current += 1
        else:
            count += min(before, current)
            before, current = current, 1
    return count + min(before, current)


def main():
    strings = []
    for k in range(20):
        longest = 1 + 2 * k
        s = []
        bit = 0
        while len(s) < 100000:
            run = 1 + next_random() % longest
            for _ in range(run):
                if len(s) < 100000:
                    s.append("0" if bit == 0 else "1")
            bit = 1 - bit
        strings.append("".join(s))
    rounds = 150
    total = 0
    checksum = 0
    for _ in range(rounds):
        for s in strings:
            r = count_binary_substrings(s)
            total += r
            checksum = (checksum * 31 + r) % 1000000007
    print(f"{rounds} rounds of 20 strings of 100000: {total} substrings counted, checksum {checksum}")


main()
