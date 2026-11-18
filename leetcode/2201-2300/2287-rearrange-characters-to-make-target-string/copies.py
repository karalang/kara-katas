# LeetCode #2287: Rearrange Characters to Make Target String -- the
# Python mirror of the ★ arm, `copies.kara`.


def rearrange_characters(s, target):
    have = [0] * 26
    need = [0] * 26
    for c in s:
        have[ord(c) - ord("a")] += 1
    for c in target:
        need[ord(c) - ord("a")] += 1
    copies = len(s)
    for i in range(26):
        if need[i] > 0:
            copies = min(copies, have[i] // need[i])
    return copies


# ---- test harness ---------------------------------------------------------

seed = 2287


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(length))


def main():
    cases = [
        ("ilovecodingonleetcode", "code"),
        ("abcba", "abc"),
        ("abbaccaddaeea", "aaaaa"),
        ("ab", "abc"),
        ("zzzzzzz", "z"),
        ("codecodecodecodecodecodecodecodecodecode", "code"),
    ]
    for s, target in cases:
        print(f"{s} {target} -> {rearrange_characters(s, target)}")
    check = 0
    total = 0
    for _ in range(3000):
        letters = next_random() % 26 + 1
        s_len = next_random() % 100 + 1
        t_len = next_random() % 10 + 1
        s = word(s_len, letters)
        target = word(t_len, letters)
        answer = rearrange_characters(s, target)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 cases: checksum {check}, {total} copies in all")


main()
