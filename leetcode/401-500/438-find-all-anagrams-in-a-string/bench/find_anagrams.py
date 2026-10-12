# Benchmark for #438: mirror of find_anagrams.kara (a sliding window of
# letter counts) on 40 patterns searched in one random text of
# 1,000,000 letters.


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
    differ = 0
    for c in range(26):
        if need[c] != 0:
            differ += 1
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


seed = 438


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 1000000
    patterns = 40
    # Letters from 'a' to 'd', so that short patterns have many
    # anagrams in the text.
    text = "".join(chr(97 + next_random() % 4) for _ in range(size))
    found = 0
    checksum = 0
    for _ in range(patterns):
        length = 1 + next_random() % 12
        p = "".join(chr(97 + next_random() % 4) for _ in range(length))
        starts = find_anagrams(text, p)
        found += len(starts)
        for i in starts:
            checksum = (checksum * 31 + i) % 1000000007
    print(f"{patterns} patterns in a text of {size}: {found} anagrams, checksum {checksum}")


main()
