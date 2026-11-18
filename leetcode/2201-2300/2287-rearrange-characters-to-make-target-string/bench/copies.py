# LeetCode #2287: Rearrange Characters to Make Target String -- the
# bench, the ★ arm's Python mirror. Two lists of 26 counts and the least
# quotient.


def rearrange_characters(s, target):
    have = [0] * 26
    need = [0] * 26
    for b in s.encode():
        have[b - 97] += 1
    for b in target.encode():
        need[b - 97] += 1
    copies = len(s)
    for i in range(26):
        if need[i] > 0:
            copies = min(copies, have[i] // need[i])
    return copies


# ---- bench harness ---------------------------------------------------------

seed = 2287


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(length))


def main():
    pairs = []
    for _ in range(10000):
        letters = next_random() % 6 + 1
        s_len = next_random() % 100 + 1
        t_len = next_random() % 10 + 1
        s = word(s_len, letters)
        target = word(t_len, letters)
        pairs.append((s, target))
    check = 0
    for _ in range(200):
        total = 0
        for s, target in pairs:
            total += rearrange_characters(s, target)
        check = (check * 31 + total) % 1000000007
    print(f"200 passes over 10^4 pairs: checksum {check}")


main()
