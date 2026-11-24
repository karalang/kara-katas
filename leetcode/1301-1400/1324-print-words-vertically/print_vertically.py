# LeetCode #1324: Print Words Vertically -- Python mirror of the ★ Kāra
# arm: the words split apart, and row i made of each word's i-th letter in
# turn, a space for a word too short to have one, with the spaces left at
# the row's end trimmed.


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


def show(s):
    return "[" + ",".join(print_vertically(s)) + "]"


def main():
    print(f'{show("HOW ARE YOU")} {show("TO BE OR NOT TO BE")} {show("CONTEST IS COMING")} {show("A")} {len(print_vertically("Q" * 200))} {show("B " * 99 + "C")}')
    seed = 1324

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    total = 0
    check = 0
    for t in range(600):
        limit = 1 + nr() % 200
        longest = 3 if t % 4 == 0 else 10 if t % 4 == 1 else 40 if t % 4 == 2 else 200
        k = 2 if t % 8 < 4 else 26
        out = []
        while True:
            ln = 1 + nr() % longest
            if out:
                if len(out) + 1 + ln > limit:
                    break
                out.append(" ")
            elif ln > limit:
                ln = limit
            for _ in range(ln):
                out.append(chr(65 + nr() % k))
        rows = print_vertically("".join(out))
        total += len(rows)
        for row in rows:
            for c in row:
                check = (check * 131 + ord(c)) % 1000000007
            check = (check * 131 + 1) % 1000000007
    print(f"600 random sentences: rows total {total}, checksum {check}")


main()
