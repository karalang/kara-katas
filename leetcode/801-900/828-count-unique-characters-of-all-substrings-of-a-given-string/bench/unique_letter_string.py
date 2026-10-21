# Benchmark for #828: Count Unique Characters of All Substrings of a Given
# String -- the ★ arm (each character's contribution).
#
# Mirrors unique_letter_string.kara: a character at i is unique in
# (i - prev) * (next - i) substrings, prev and next the copies of its
# letter beside it; one pass keeps the last two positions of each letter
# and settles the middle one each time a letter recurs.


def unique_letter_string(s):
    n = len(s)
    last = [-1] * 26
    before = [-1] * 26
    total = 0
    for i in range(n):
        c = ord(s[i]) - 65
        if last[c] >= 0:
            total += (last[c] - before[c]) * (i - last[c])
        before[c] = last[c]
        last[c] = i
    for c in range(26):
        if last[c] >= 0:
            total += (last[c] - before[c]) * (n - last[c])
    return total


def main():
    count, rounds, n = 32, 12800, 100000
    seed = 828

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for g in range(count):
        letters = 1 + g % 26
        strings.append("".join(chr(65 + next_random() % letters) for _ in range(n)))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        r = unique_letter_string(strings[rnd % count])
        total += r
        checksum = (checksum * 131 + r) % 1000000007
    print(f"{rounds} rounds of {count} strings: total {total}, checksum {checksum}")


main()
