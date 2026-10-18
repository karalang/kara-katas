# LeetCode #696: Count Binary Substrings -- two run lengths.
#
# A mirror of count_binary_substrings.kara (the ★ arm) and its harness.


def count_binary_substrings(s):
    before, current, count = 0, 1, 0
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            current += 1
        else:
            count += min(before, current)
            before, current = current, 1
    return count + min(before, current)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_runs(n, longest):
    s = []
    bit = next_random() % 2
    while len(s) < n:
        run = 1 + next_random() % longest
        for _ in range(run):
            if len(s) < n:
                s.append("0" if bit == 0 else "1")
        bit = 1 - bit
    return "".join(s)


def main():
    global seed
    f = count_binary_substrings
    print(f"example 1: {f('00110011')}")
    print(f"example 2: {f('10101')}")
    print(f"0: {f('0')}, 01: {f('01')}, 0000: {f('0000')}")
    print(f"000111: {f('000111')}, 0001111: {f('0001111')}")
    blocks = "0" * 2000 + "1" * 2000
    alternating = "".join("1" if i % 2 == 0 else "0" for i in range(100000))
    print(f"two blocks of 2000: {f(blocks)}, 100000 alternating: {f(alternating)}")
    seed = 696
    print(f"100000 in runs of up to 20: {f(random_runs(100000, 20))}")
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 2000
        longest = 1 + next_random() % 50
        r = f(random_runs(n, longest))
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"300 random strings: {total} substrings in all, checksum {checksum}")


main()
