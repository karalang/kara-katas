# LeetCode #1371: Find the Longest Substring Containing Vowels in Even
# Counts -- Python mirror of the ★ arm: each vowel's count kept as a
# parity bit, and the answer the furthest apart two prefixes with the
# same bits are.

BIT = {"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}


def find_the_longest_substring(s):
    first = [-2] * 32
    first[0] = -1
    bits = 0
    best = 0
    for i, c in enumerate(s):
        bits ^= BIT.get(c, 0)
        if first[bits] == -2:
            first[bits] = i
        else:
            best = max(best, i - first[bits])
    return best


seed = 1371


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cycle = "".join(chr(97 + i % 26) for i in range(2000))
    print(" ".join(str(find_the_longest_substring(s)) for s in ["eleetminicoworoep", "leetcodeisgreat", "bcbcbc", "a", "aa", cycle]))
    pool = "aeioubcxyz"
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        kinds = 1 + next_random() % 11
        out = []
        for _ in range(n):
            r = next_random()
            out.append(chr(97 + r % 26) if kinds == 11 else pool[r % kinds])
        got = find_the_longest_substring("".join(out))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random strings: lengths total {total}, checksum {check}")


main()
