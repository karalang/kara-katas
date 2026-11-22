# LeetCode #2825: Make String a Subsequence Using Cyclic Increments --
# the bench's Python mirror of the ★ arm: two pointers over the bytes,
# each letter of str1 as it is or once incremented taking str2's next
# letter.


def can_make_subsequence(str1, str2):
    a, b = str1.encode(), str2.encode()
    j = 0
    for c in a:
        if j == len(b):
            break
        nxt = ord("a") if c == ord("z") else c + 1
        if c == b[j] or nxt == b[j]:
            j += 1
    return j == len(b)


seed = 2825


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, start, width):
    return "".join(chr((start + next_random() % width) % 26 + 97) for _ in range(n))


def main():
    count, rounds = 100, 50
    pairs = []
    for _ in range(count):
        s1 = letters(100000, 23, 6)
        m = (next_random() * 32768 + next_random()) % 50000 + 1
        pairs.append((s1, letters(m, 23, 6)))
    yes = 0
    check = 0
    for r in range(rounds):
        for s1, s2 in pairs:
            a = can_make_subsequence(s1, s2)
            yes += a
            check = (check * 31 + (1 if a else 0) + r) % 1000000007
    print(f"{count} pairs of 100000, {rounds} rounds: {yes} true, checksum {check}")


main()
