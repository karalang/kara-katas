# LeetCode #1520: Maximum Number of Non-Overlapping Substrings -- the
# bench in Python: the ★ arm over 200000 random strings of 1 to 64
# letters over 5, built once and answered 3 times.


def max_num_of_substrings(s):
    b = s.encode()
    n = len(b)
    first = [n] * 26
    last = [-1] * 26
    for i in range(n):
        c = b[i] - 97
        first[c] = min(first[c], i)
        last[c] = i
    spans = []
    right = -1
    for i in range(n):
        c = b[i] - 97
        if i != first[c]:
            continue
        end = last[c]
        ok = True
        j = i
        while j <= end:
            d = b[j] - 97
            if first[d] < i:
                ok = False
                break
            end = max(end, last[d])
            j += 1
        if not ok:
            continue
        if i > right:
            spans.append((i, end))
        else:
            spans[-1] = (i, end)
        right = end
    return [s[a:e + 1] for a, e in spans]


def main():
    seed = 1520

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for _ in range(200000):
        n = next_random() % 64 + 1
        strings.append("".join(chr(97 + next_random() % 5) for _ in range(n)))
    check = 0
    pieces = 0
    for _ in range(3):
        for s in strings:
            for piece in max_num_of_substrings(s):
                pieces += 1
                check = (check * 31 + len(piece) + 1) % 1000000007
                check = (check * 31 + ord(piece[0]) + 1) % 1000000007
    print(f"3 passes over 200000 strings of up to 64 letters: {pieces} substrings, checksum {check}")


main()
