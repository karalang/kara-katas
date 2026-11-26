# LeetCode #1781: Sum of Beauty of All Substrings -- the bench in Python,
# mirroring beauty_sum.kara: the letters' counts grown from each start.


def beauty_sum(s):
    n = len(s)
    total = 0
    for i in range(n):
        counts = [0] * 26
        for j in range(i, n):
            counts[ord(s[j]) - 97] += 1
            most, fewest = 0, n
            for c in counts:
                if c > 0:
                    most = max(most, c)
                    fewest = min(fewest, c)
            total += most - fewest
    return total


seed = 1781


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    words = []
    for w in range(48):
        letters = 2 + w % 12 * 2
        words.append("".join(chr(97 + next_random() % letters) for _ in range(500)))
    check = 0
    for w in range(48):
        check = (check * 31 + beauty_sum(words[w])) % 1000000007
    print(f"48 strings of 500 letters: checksum {check}")


main()
