# LeetCode #647: Palindromic Substrings -- Python mirror of the Kāra
# bench.
#
# The ★ arm over the same texts and rounds: from each of the 2n - 1
# centers, the window widened while its two ends match, over the str.


def count_substrings(s):
    n = len(s)
    count = 0
    for center in range(2 * n - 1):
        lo = center // 2
        hi = lo + center % 2
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            count += 1
            lo -= 1
            hi += 1
    return count


seed = 647


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 20
    rounds = 300
    texts = []
    for _ in range(inputs):
        letters = 1 + next_random() % 3
        texts.append("".join(chr(97 + next_random() % letters) for _ in range(2000)))
    total = 0
    checksum = 0
    for r in range(rounds):
        c = count_substrings(texts[(r * 7) % inputs])
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: total {total}, checksum {checksum}")


main()
