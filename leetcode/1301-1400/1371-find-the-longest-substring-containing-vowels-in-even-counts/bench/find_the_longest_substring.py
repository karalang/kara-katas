# LeetCode #1371 bench -- Python: each vowel's count kept as a parity bit,
# and the answer the furthest apart two prefixes with the same bits are.

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
    # 4 strings of 5 * 10^5 letters, the constraints' most, drawn from
    # "aeioubcxyz", built once; then 80 rounds, each changing one letter
    # of one string to a copy, both drawn from the checksum so far, and
    # finding that string's longest substring
    pool = "aeioubcxyz"
    strings = ["".join(pool[next_random() % 10] for _ in range(500000)) for _ in range(4)]
    check = 0
    for r in range(80):
        i = check % 4
        at = (check // 4) % 500000
        s = strings[i]
        strings[i] = s[:at] + pool[(check // 2000000) % 10] + s[at + 1:]
        got = find_the_longest_substring(strings[i])
        check = (check * 31 + got + r) % 1000000007
    print(f"80 rounds over 4 strings of 500000 letters: checksum {check}")


main()
