# LeetCode #2083: Substrings That Begin and End With the Same Letter --
# Python mirror of the ★ arm's benchmark (same.kara): one text of 10^6
# letters built once, then 5000 windows of 10^5 letters, each copied out of
# the text by slicing and counted.

seed = 2083


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_substrings(s):
    counts = [0] * 26
    for b in s:
        counts[b - 97] += 1
    return sum(c * (c + 1) // 2 for c in counts)


def main():
    letters = b"abcdefghijklmnopqrstuvwxyz"
    out = bytearray()
    for _ in range(1000000):
        at = next_random() % 26
        at = at * (next_random() % 26) // 25
        out.append(letters[at])
    text = bytes(out)
    total = 0
    check = 0
    for _ in range(5000):
        start = next_random() * 32768
        start = (start + next_random()) % 900001
        a = number_of_substrings(text[start:start + 100000])
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"5000 windows: sum {total}, checksum {check}")


main()
