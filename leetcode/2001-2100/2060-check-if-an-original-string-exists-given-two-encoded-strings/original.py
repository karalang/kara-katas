# LeetCode #2060: Check if an Original String Exists Given Two Encoded
# Strings -- Python mirror of the ★ arm (original.kara): a depth-first
# search over (place in s1, place in s2, lead of s1 over s2), each state
# tried once.

import sys

sys.setrecursionlimit(10000)


def possibly_equals(s1, s2):
    seen = set()

    def search(i, j, lead):
        if i == len(s1) and j == len(s2):
            return lead == 0
        if (i, j, lead) in seen:
            return False
        seen.add((i, j, lead))
        if i < len(s1) and s1[i].isdigit():
            num = 0
            k = i
            while k < len(s1) and s1[k].isdigit():
                num = num * 10 + int(s1[k])
                k += 1
                if search(k, j, lead + num):
                    return True
            return False
        if j < len(s2) and s2[j].isdigit():
            num = 0
            k = j
            while k < len(s2) and s2[k].isdigit():
                num = num * 10 + int(s2[k])
                k += 1
                if search(i, k, lead - num):
                    return True
            return False
        if lead > 0:
            return j < len(s2) and search(i, j + 1, lead - 1)
        if lead < 0:
            return i < len(s1) and search(i + 1, j, lead + 1)
        return i < len(s1) and j < len(s2) and s1[i] == s2[j] and search(i + 1, j + 1, 0)

    return search(0, 0, 0)


# ---- test harness

seed = 2060


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def encode(orig):
    """Some pieces of `orig` replaced by their lengths, no digit run longer
    than three and no length with a 0 in it."""
    out = ""
    run = 0
    i = 0
    while i < len(orig):
        piece = min(next_random() % 12 + 1, len(orig) - i)
        text = str(piece)
        if next_random() % 2 == 0 and "0" not in text and run + len(text) <= 3:
            out += text
            run += len(text)
        else:
            out += orig[i:i + piece]
            run = 0
        i += piece
    return out


def main():
    examples = [
        ("internationalization", "i18n"),
        ("l123e", "44"),
        ("a5b", "c5b"),
        ("112s", "g841"),
        ("ab", "a2"),
        ("1", "z"),
        ("a", "b"),
        ("98u8v8v8v89u888u998v88u98v88u9v99u989v8u", "9v898u98v888v89v998u98v9v888u9v899v998u9"),
    ]
    for s1, s2 in examples:
        print(f"{s1}, {s2} -> {str(possibly_equals(s1, s2)).lower()}")
    possible = 0
    check = 0
    for t in range(3000):
        n = next_random() % 40 + 1
        k = next_random() % 3 + 1
        orig = letters(n, k)
        if t % 3 == 0:
            other = orig
        elif t % 3 == 1:
            other = letters(n, k)
        else:
            at = next_random() % n
            other = orig[:at] + orig[at + 1:] if next_random() % 2 == 0 else orig + letters(1, k)
            if other == "":
                other = letters(1, k)
        s1 = encode(orig)
        s2 = encode(other)
        ok = possibly_equals(s1, s2)
        if ok:
            possible += 1
        check = (check * 31 + (2 if ok else 1)) % 1000000007
    print(f"3000 pairs: {possible} possible, checksum {check}")


main()
