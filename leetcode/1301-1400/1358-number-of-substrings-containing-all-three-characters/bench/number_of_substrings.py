# LeetCode #1358 -- bench, Python: where each of a, b and c was last seen;
# a substring ending at i holds all three when it starts at or before the
# earliest of those places.


def number_of_substrings(s):
    last = [-1, -1, -1]
    count = 0
    for i, b in enumerate(s):
        last[b - 97] = i
        count += min(last) + 1
    return count


seed = [1358]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 20 strings of 5 * 10^4 letters, the constraints' most, c drawn one
    # time in 1000 and a and b evenly, built once; then 1000 rounds, each
    # setting one letter of one string, both drawn from the checksum so
    # far, and counting that string's substrings
    texts = []
    for _ in range(20):
        text = bytearray()
        for _ in range(50000):
            r = next_random() % 1000
            text.append(99 if r == 0 else 97 if r % 2 == 0 else 98)
        texts.append(text)
    check = 0
    for r in range(1000):
        k = check % 20
        texts[k][(check // 20) % 50000] = 97 + (check // 7) % 3
        check = (check * 31 + number_of_substrings(texts[k]) + r) % 1000000007
    print(f"1000 rounds over 20 strings of 5 * 10^4 letters: checksum {check}")


main()
