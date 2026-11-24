# LeetCode #1320 bench, Python mirror of the Kāra bench: the ★ arm (one row
# of 27 for the other finger's key, carried from letter to letter) on 100
# words of 300 letters over 2, 5 or 26 letters, built once; then 80 passes,
# each setting one letter of every word from the checksum so far, answering
# it and folding the answer plus the pass into the checksum.


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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed = 1320

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    words = []
    for t in range(100):
        k = 2 if t % 3 == 0 else 5 if t % 3 == 1 else 26
        base = nr() % (27 - k)
        words.append([letters[base + nr() % k] for _ in range(300)])
    check = 0
    for p in range(80):
        for t in range(100):
            chars = words[t]
            chars[check % 300] = letters[(check // 7) % 26]
            got = minimum_distance("".join(chars))
            check = (check * 31 + got + p) % 1000000007
    print(f"80 passes over 100 words of 300: checksum {check}")


main()
