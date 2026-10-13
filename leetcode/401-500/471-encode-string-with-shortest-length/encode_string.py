# LeetCode #471: Encode String with Shortest Length -- Python mirror of
# the ★ arm (encode_string.kara): interval DP over the encodings, with
# the shortest unit found where t first appears again in t + t.


def encode(s):
    n = len(s)
    best = [["" for _ in range(n)] for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            t = s[i:j + 1]
            doubled = t + t
            unit = 1 + doubled[1:].find(t)
            shortest = t
            if unit < length:
                packed = f"{length // unit}[{best[i][i + unit - 1]}]"
                if len(packed) < len(shortest):
                    shortest = packed
            for k in range(i, j):
                if len(best[i][k]) + len(best[k + 1][j]) < len(shortest):
                    shortest = best[i][k] + best[k + 1][j]
            best[i][j] = shortest
    return best[0][n - 1]


# ---- test harness ---------------------------------------------------------

def expand(cs, pos):
    out = []
    while pos[0] < len(cs) and cs[pos[0]] != "]":
        c = cs[pos[0]]
        if c.isdigit():
            k = 0
            while pos[0] < len(cs) and cs[pos[0]].isdigit():
                k = k * 10 + ord(cs[pos[0]]) - 48
                pos[0] += 1
            if k < 1 or pos[0] >= len(cs) or cs[pos[0]] != "[":
                return None
            pos[0] += 1
            inner = expand(cs, pos)
            if inner is None:
                return None
            if pos[0] >= len(cs):
                return None
            pos[0] += 1
            out.append(inner * k)
        elif c == "[":
            return None
        else:
            out.append(c)
            pos[0] += 1
    return "".join(out)


def decode(e):
    pos = [0]
    out = expand(e, pos)
    if out is None or pos[0] != len(e):
        return None
    return out


def show(label, s):
    e = encode(s)
    back = decode(e) == s
    print(f"{label} -> length {len(e)}, decodes back: {str(back).lower()}, unchanged: {str(e == s).lower()}")


seed = 471


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(letters, depth):
    s = []
    pieces = 1 + next_random() % 4
    for _ in range(pieces):
        if depth > 0 and next_random() % 2 == 0:
            unit = random_string(letters, depth - 1)
            copies = 2 + next_random() % 11
            s.append(unit * copies)
        else:
            s.append(chr(97 + next_random() % letters))
    return "".join(s)


def main():
    for s in ["aaa", "aaaaa", "aaaaaaaaaa", "aabcaabcd", "abbbabbbcabbbabbbc", "a", "aaaa", "ababab", "abcdef", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"]:
        show(f"\"{s}\"", s)
    show("150 a's", "a" * 150)
    show("50 abc's", "abc" * 50)
    show("abcdefghijklmnopqrstuvwxy written 6 times", "abcdefghijklmnopqrstuvwxy" * 6)
    show("ab, 74 times, then a", "ab" * 74 + "a")
    count = 300
    total = 0
    unchanged = 0
    all_back = True
    checksum = 0
    for _ in range(count):
        letters = 1 + next_random() % 3
        full = random_string(letters, 2)
        cut = 1 + next_random() % 60
        s = full[:cut] if len(full) > cut else full
        e = encode(s)
        total += len(e)
        if e == s:
            unchanged += 1
        all_back = all_back and decode(e) == s
        checksum = (checksum * 31 + len(e)) % 1000000007
    print(f"{count} random strings: {total} letters encoded, {unchanged} unchanged, all decode back: {str(all_back).lower()}, checksum {checksum}")


main()
