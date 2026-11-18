# LeetCode #1624: Largest Substring Between Two Equal Characters -- the
# Python mirror of gap.kara (★).
#
# One pass: the first index of each letter, and at every later sight of
# it the gap back to that first index.


def max_length_between_equal_characters(s):
    first = [-1] * 26
    best = -1
    for i, c in enumerate(s):
        letter = ord(c) - ord("a")
        if first[letter] == -1:
            first[letter] = i
        else:
            best = max(best, i - first[letter] - 1)
    return best


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, longest, letters):
    check = 0
    none = 0
    for _ in range(count):
        n = next_random() % longest + 1
        s = "".join(chr(ord("a") + next_random() % letters) for _ in range(n))
        got = max_length_between_equal_characters(s)
        if got == -1:
            none += 1
        check = mix(check, got)
    print(f"{count} strings of up to {longest} letters from {letters}: {none} with no pair, checksum {check}")


def main():
    global seed
    for s in ["aa", "abca", "cbzxy", "a", "abcdefghijklmnopqrstuvwxyza"]:
        print(max_length_between_equal_characters(s))
    print(max_length_between_equal_characters("q" + "z" * 298 + "q"))
    seed = 1624
    batch(3000, 8, 3)
    batch(3000, 30, 26)
    batch(300, 300, 26)


main()
