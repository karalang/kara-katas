# LeetCode #1324 bench, Python mirror of the Kāra bench: the ★ arm (the
# words split apart, row i made of each word's i-th letter or a space, the
# row's end trimmed) on 100 sentences of 200 letters and spaces built once;
# then 1000 passes, each setting one letter of every sentence from the
# checksum so far, answering it and folding the rows' letters plus the pass
# into the checksum.


def print_vertically(s):
    words = s.split(" ")
    tallest = max(len(w) for w in words)
    rows = []
    for i in range(tallest):
        row = []
        for w in words:
            row.append(w[i] if i < len(w) else " ")
        rows.append("".join(row).rstrip(" "))
    return rows


seed = 1324


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 200
    sentences = []
    for t in range(100):
        longest = 3 if t % 4 == 0 else 10 if t % 4 == 1 else 40 if t % 4 == 2 else 200
        b = []
        while len(b) < n:
            ln = 1 + next_random() % longest
            for _ in range(ln):
                if len(b) < n:
                    b.append(65 + next_random() % 26)
            if len(b) < n - 1:
                b.append(32)
        sentences.append(b)
    check = 0
    for p in range(1000):
        for t in range(100):
            b = sentences[t]
            at = check % n
            if b[at] != 32:
                b[at] = 65 + check // 7 % 26
            rows = print_vertically(bytes(b).decode())
            for row in rows:
                for c in row.encode():
                    check = (check * 131 + c) % 1000000007
            check = (check * 31 + len(rows) + p) % 1000000007
    print(f"1000 passes over 100 sentences of 200: checksum {check}")


main()
