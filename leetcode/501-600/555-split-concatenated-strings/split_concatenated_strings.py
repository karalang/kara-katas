# LeetCode #555: Split Concatenated Strings -- Python mirror of the ★ arm
# (every cut, the rest at its best); see split_concatenated_strings.kara.


def split_loop(strs):
    n = len(strs)
    larger = []
    for s in strs:
        r = s[::-1]
        larger.append(r if r > s else s)
    answer = ""
    for i in range(n):
        middle = "".join(larger[(i + j) % n] for j in range(1, n))
        for t in (strs[i], strs[i][::-1]):
            for k in range(len(t)):
                candidate = t[k:] + middle + t[:k]
                if candidate > answer:
                    answer = candidate
    return answer


# ---- test harness ---------------------------------------------------------

seed = 555


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(strs):
    print(f"[{', '.join(strs)}] -> {split_loop(strs)}")


def word(length, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(length))


def checksum(text):
    h = 0
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    show(["abc", "xyz"])
    show(["abc"])
    show(["a"])
    show(["zz", "zz"])
    show(["ab", "ba", "ab"])
    show(["lc", "evol", "cdy"])
    show(["zab", "zza", "bz"])
    letters = 0
    h = 0
    for _ in range(300):
        n = 1 + next_random() % 6
        alphabet = 2 + next_random() % 25
        strs = []
        for _ in range(n):
            length = 1 + next_random() % 6
            strs.append(word(length, alphabet))
            letters += length
        for b in split_loop(strs).encode():
            h = (h * 31 + b) % 1000000007
    print(f"300 random lists: {letters} letters, checksum {h}")
    many = [word(1, 26) for _ in range(1000)]
    one = [word(1000, 26)]
    tens = [word(10, 2) for _ in range(100)]
    for strs in (many, one, tens):
        got = split_loop(strs)
        print(f"{len(got)} letters, starting {got[:12]}, checksum {checksum(got)}")


main()
