# LeetCode #2060: Check if an Original String Exists Given Two Encoded
# Strings -- Python mirror of the ★ arm's benchmark (original.kara): the
# same 2000 pairs, each answered by one search over (place, place, lead)
# with a set of the states tried.
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


seed = 2060


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def dense():
    s = ""
    while True:
        run = "".join(chr(ord("1") + next_random() % 9) for _ in range(next_random() % 3 + 1))
        letter = "u" if next_random() % 2 == 0 else "v"
        if len(s) + len(run) + 1 > 40:
            return s
        s += run + letter


def main():
    possible = 0
    check = 0
    for _ in range(2000):
        s1 = dense()
        s2 = dense()
        ok = possibly_equals(s1, s2)
        if ok:
            possible += 1
        check = (check * 31 + (2 if ok else 1)) % 1000000007
    print(f"2000 pairs: {possible} possible, checksum {check}")


main()
