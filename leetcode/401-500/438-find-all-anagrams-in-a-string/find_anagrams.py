# LeetCode #438: Find All Anagrams in a String -- mirror of
# find_anagrams.kara (a sliding window of letter counts).


def find_anagrams(s, p):
    sb = s.encode()
    pb = p.encode()
    n = len(sb)
    m = len(pb)
    starts = []
    if m > n:
        return starts
    # need[c] is p's count of c minus the window's.
    need = [0] * 26
    for i in range(m):
        need[pb[i] - 97] += 1
    differ = sum(1 for c in range(26) if need[c] != 0)
    for i in range(n):
        enter = sb[i] - 97
        if need[enter] == 0:
            differ += 1
        need[enter] -= 1
        if need[enter] == 0:
            differ -= 1
        if i >= m:
            leave = sb[i - m] - 97
            if need[leave] == 0:
                differ += 1
            need[leave] += 1
            if need[leave] == 0:
                differ -= 1
        if i >= m - 1 and differ == 0:
            starts.append(i - m + 1)
    return starts


def show(s, p):
    starts = find_anagrams(s, p)
    print(f"\"{s}\", \"{p}\": [{','.join(str(i) for i in starts)}]")


seed = 438


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("cbaebabacd", "abc")
    show("abab", "ab")
    show("a", "a")
    show("a", "ab")
    show("aaaaa", "aa")
    show("abcdefg", "gfedcba")
    show("zyxzyxzyx", "xyz")
    show("abcabc", "d")
    show("baa", "aa")
    # 300 random pairs over a 1, 2, 3 or 26 letter alphabet: s of 1 to
    # 80 letters and p of 1 to 6.
    found = 0
    checksum = 0
    for _ in range(300):
        letters = [1, 2, 3, 26][next_random() % 4]
        n = 1 + next_random() % 80
        m = 1 + next_random() % 6
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        p = "".join(chr(97 + next_random() % letters) for _ in range(m))
        for i in find_anagrams(s, p):
            found += 1
            checksum = (checksum * 31 + i + 1) % 1000000007
        checksum = (checksum * 31) % 1000000007
    print(f"300 random pairs: {found} anagrams, checksum {checksum}")


main()
