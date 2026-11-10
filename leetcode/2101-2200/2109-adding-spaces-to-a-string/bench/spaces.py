# LeetCode #2109: Adding Spaces to a String -- the benchmark, the same
# algorithm as spaces.kara: one walk over the letters with an index into
# the spaces.


def add_spaces(s, spaces):
    out = []
    nxt = 0
    for i, c in enumerate(s):
        if nxt < len(spaces) and spaces[nxt] == i:
            out.append(" ")
            nxt += 1
        out.append(c)
    return "".join(out)


seed = 2109


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rows = []
    for _ in range(20):
        s = []
        spaces = []
        for i in range(300000):
            s.append(letters[next_random() % 52])
            if next_random() % 3 == 0:
                spaces.append(i)
        rows.append(("".join(s), spaces))
    total = 0
    check = 0
    for s, spaces in rows:
        for _ in range(5):
            got = add_spaces(s, spaces)
            total += len(got)
            b = got.encode()
            for j in range(0, len(b), 997):
                check = (check * 31 + b[j]) % 1000000007
    print(f"100 strings: {total} characters, checksum {check}")


main()
