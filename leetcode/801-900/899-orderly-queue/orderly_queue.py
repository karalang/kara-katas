# LeetCode #899: Orderly Queue -- Python mirror of the every-rotation
# solution in orderly_queue.kara, with the same test harness.
#
# With k = 1 the only move takes the first letter to the end, so the
# strings reachable are the rotations of s: build each and keep the
# smallest. With k >= 2 the first two letters can be sent to the end in
# either order, which (with rotating) swaps any two neighbours, so every
# order of the letters is reachable and the answer is them sorted.
# O(n^2) for k = 1, O(n log n) otherwise.


def orderly_queue(s, k):
    n = len(s)
    if k == 1:
        best = s
        for i in range(1, n):
            r = "".join(s[(i + j) % n] for j in range(n))
            if r < best:
                best = r
        return best
    return "".join(sorted(s))


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, k):
    print(f"s = \"{s}\", k = {k} -> \"{orderly_queue(s, k)}\"")


# `len` random letters from the first `letters` of the alphabet; with
# `repeat`, a random piece of up to 5 letters written over and over
def random_string(length, letters, repeat):
    p = 1 + next_random() % 5
    piece = [chr(97 + next_random() % letters) for _ in range(p)]
    out = []
    for i in range(length):
        if repeat:
            out.append(piece[i % p])
        else:
            out.append(chr(97 + next_random() % letters))
    return "".join(out)


def checksum(s, check):
    for ch in s:
        check = (check * 131 + ord(ch)) % 1000000007
    return check


def main():
    global seed
    show("cba", 1)
    show("baaca", 3)
    show("a", 1)
    show("aaaa", 1)
    show("bab", 1)
    show("bab", 2)
    show("abab", 1)
    show("dcba", 4)
    show("zyxwvutsrqponmlkjihgfedcba", 1)
    show("zyxwvutsrqponmlkjihgfedcba", 2)
    # random cases of up to 300 letters from 1 to 26 letters, half of
    # them with k = 1, a quarter of them a short piece repeated
    seed = 899
    check = 0
    letters_in_all = 0
    for c in range(300):
        length = 1 + next_random() % 300
        letters = 1 + next_random() % 26
        s = random_string(length, letters, c % 4 == 0)
        k = 1 if c % 2 == 0 else 1 + next_random() % length
        check = checksum(orderly_queue(s, k), check)
        letters_in_all += length
    print(f"300 cases of up to 300 letters ({letters_in_all} letters): checksum {check}")
    # LeetCode's largest: 1000 letters, a repeated piece with one letter
    # changed near the end, k = 1; and 1000 random letters, k = 2
    big = "".join("a" if i == 991 else ("a" if i % 3 == 0 else "b") for i in range(1000))
    print(f"1000 letters, k = 1 -> checksum {checksum(orderly_queue(big, 1), 0)}")
    srt = orderly_queue(random_string(1000, 26, False), 2)
    print(f"1000 random letters, k = 2 -> checksum {checksum(srt, 0)}")


main()
