# LeetCode #2486: Append Characters to String to Make Subsequence --
# bench, Python mirror of append.kara.


def append_characters(s, t):
    matched = 0
    for c in s:
        if matched < len(t) and c == t[matched]:
            matched += 1
    return len(t) - matched


seed = 2486


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = ['a', 'b', 'c', 'd']
    pairs = []
    for _ in range(20):
        s = [letters[next_random() % 4] for _ in range(10000)]
        t = "".join(letters[next_random() % 4] for _ in range(10000))
        pairs.append((s, t))
    check = 0
    for p in range(600):
        for g in range(20):
            pairs[g][0][check % 10000] = letters[check // 10000 % 4]
            s = "".join(pairs[g][0])
            check = (check * 31 + append_characters(s, pairs[g][1]) + p) % 1000000007
    print(f"600 passes over 20 pairs of 10^4 letters: checksum {check}")


main()
