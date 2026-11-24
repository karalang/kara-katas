# LeetCode #1320: Minimum Distance to Type a Word Using Two Fingers --
# Python mirror of the ★ Kāra arm: after each letter one finger is on it,
# so all that matters is where the other finger is, one of 26 keys or not
# yet placed; the least distance for each, one row of 27 carried from
# letter to letter.


def key_distance(a, b):
    if a == 26:
        return 0
    return abs(a // 6 - b // 6) + abs(a % 6 - b % 6)


def minimum_distance(word):
    w = [b - 65 for b in word.encode()]
    free = 26
    far = 1000000
    other = [far] * 27
    other[free] = 0
    for i in range(1, len(w)):
        last, now = w[i - 1], w[i]
        nxt = [far] * 27
        for j in range(27):
            if other[j] < far:
                nxt[j] = min(nxt[j], other[j] + key_distance(last, now))
                nxt[last] = min(nxt[last], other[j] + key_distance(j, now))
        other = nxt
    return min(other)


def main():
    ask = minimum_distance
    print(f"{ask('CAKE')} {ask('HAPPY')} {ask('AZ')} {ask('QQQQ')} {ask('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} {ask('AZ' * 150)}")
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed = 1320

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    total = 0
    check = 0
    for t in range(400):
        n = 2 + nr() % 299
        k = 2 if t % 3 == 0 else 5 if t % 3 == 1 else 26
        base = nr() % (27 - k)
        word = "".join(letters[base + nr() % k] for _ in range(n))
        got = minimum_distance(word)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"400 random words: distance total {total}, checksum {check}")


main()
