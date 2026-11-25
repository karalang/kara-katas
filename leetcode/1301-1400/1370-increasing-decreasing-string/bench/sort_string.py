# LeetCode #1370 bench -- Python: the letters counted, then sweeps up from
# a to z and down from z to a, each taking one of every letter still
# left, until none is.


def sort_string(s):
    counts = [0] * 26
    for b in s.encode():
        counts[b - 97] += 1
    out = []
    left = len(s)
    while left > 0:
        for i in range(26):
            if counts[i] > 0:
                out.append(chr(97 + i))
                counts[i] -= 1
                left -= 1
        for i in range(25, -1, -1):
            if counts[i] > 0:
                out.append(chr(97 + i))
                counts[i] -= 1
                left -= 1
    return "".join(out)


seed = 1370


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 strings of 500 letters, the constraints' most, each from the
    # first 2 to 26 letters of the alphabet, built once; then 60000
    # rounds, each changing one letter of one string and sorting that
    # string, all drawn from the checksum so far
    strings = []
    for k in range(20):
        letters = 2 + k * 24 // 19
        strings.append("".join(chr(97 + next_random() % letters) for _ in range(500)))
    check = 0
    for r in range(60000):
        i = check % 20
        at = (check // 20) % 500
        s = strings[i]
        strings[i] = s[:at] + chr(97 + (check // 10000) % 26) + s[at + 1:]
        for b in sort_string(strings[i]).encode():
            check = (check * 31 + b) % 1000000007
        check = (check + r) % 1000000007
    print(f"60000 rounds over 20 strings of 500 letters: checksum {check}")


main()
