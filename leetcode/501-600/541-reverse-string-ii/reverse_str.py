# LeetCode #541: Reverse String II -- Python mirror of the ★ arm (two
# pointers over the characters); see reverse_str.kara.


def reverse_str(s, k):
    chars = list(s)
    n = len(chars)
    start = 0
    while start < n:
        i, j = start, min(start + k, n) - 1
        while i < j:
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1
        start += 2 * k
    return "".join(chars)


# ---- test harness ---------------------------------------------------------

seed = 541


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def mix(h, w):
    for b in w.encode():
        h = (h * 31 + b) % 1000000007
    return h


def show(s, k):
    print(f'"{s}", k = {k} -> "{reverse_str(s, k)}"')


def main():
    show("abcdefg", 2)
    show("abcd", 2)
    show("a", 1)
    show("abcdef", 1)
    show("abcdef", 3)
    show("abcdef", 6)
    show("abcdef", 10)
    show("abcdefghijk", 4)
    count = 300
    total = 0
    h = 0
    for _ in range(count):
        n = 1 + next_random() % 60
        k = 1 + next_random() % 70
        w = random_word(n, 26)
        total += n
        h = mix(h, reverse_str(w, k))
    print(f"{count} random words: {total} letters, checksum {h}")
    w = random_word(10000, 26)
    for k in [1, 7, 100, 4999, 5000, 10000]:
        r = reverse_str(w, k)
        print(f"10000 letters, k = {k}: starts {r[0:12]}, ends {r[9988:10000]}, checksum {mix(0, r)}")


main()
