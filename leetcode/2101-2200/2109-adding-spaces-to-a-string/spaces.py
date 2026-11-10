# LeetCode #2109: Adding Spaces to a String -- Python mirror of
# spaces.kara: one walk over the letters with their places, a second
# index into `spaces`, the space going first when it is due. O(n + k).


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
    examples = [
        ("LeetcodeHelpsMeLearn", [8, 13, 15]),
        ("icodeinpython", [1, 5, 7, 9]),
        ("spacing", [0, 1, 2, 3, 4, 5, 6]),
        ("Kara", [0]),
        ("Kara", [3]),
        ("x", [0]),
    ]
    for s, spaces in examples:
        print(f'"{s}" [{", ".join(map(str, spaces))}] -> "{add_spaces(s, spaces)}"')
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 30 + 1
        s = []
        spaces = []
        for i in range(n):
            s.append(letters[next_random() % 52])
            if next_random() % 3 == 0:
                spaces.append(i)
        if not spaces:
            spaces.append(next_random() % n)
        got = add_spaces("".join(s), spaces)
        total += len(got)
        for c in got:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"3000 strings: {total} characters, checksum {check}")
    s = "".join(letters[i % 52] for i in range(300000))
    spaced = add_spaces(s, list(range(300000)))
    print(f"every letter -> {len(spaced)} characters, {spaced.count(' ')} spaces")
    spaced = add_spaces(s, [i * 1000 for i in range(300)])
    print(f'every thousandth -> {len(spaced)} characters, ends "{spaced[-12:]}"')


main()
