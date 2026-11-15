# LeetCode #1163: Last Substring in Lexicographical Order -- Python mirror of
# the Kāra ★ arm: two pointers over the bytes, the answer copied out.


def last_substring(s):
    b = s.encode()
    n = len(b)
    i, j, k = 0, 1, 0
    while j + k < n:
        if b[i + k] == b[j + k]:
            k += 1
        elif b[i + k] > b[j + k]:
            j = j + k + 1
            k = 0
        else:
            i = max(i + k + 1, j)
            j = i + 1
            k = 0
    return s[i:]


seed = 1163


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make(kind):
    n = 400000
    block = [chr(ord("a") + next_random() % 26) for _ in range(7)]
    out = []
    for i in range(n):
        if kind == 0:
            out.append(chr(ord("a") + next_random() % 26))
        elif kind == 1:
            out.append(chr(ord("a") + next_random() % 2))
        elif kind == 2:
            out.append(chr(ord("a") + next_random() % 26) if next_random() % 1000 == 0 else block[i % 7])
        else:
            out.append("y" if next_random() % 10 == 0 else "z")
    return "".join(out)


def main():
    texts = [make(k % 4) for k in range(8)]
    total = 0
    check = 0
    for _ in range(150):
        for t in texts:
            frm = next_random() % (len(t) // 2)
            rest = t[frm:]
            got = last_substring(rest)
            total += len(got)
            check = (check * 31 + (len(rest) - len(got)) * 7 + len(got)) % 1000000007
    print(f"150 rounds over 8 strings of 4 * 10^5 letters: total {total}, checksum {check}")


main()
