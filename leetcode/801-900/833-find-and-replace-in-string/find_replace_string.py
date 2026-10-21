# Python mirror of the ★ arm plus harness for kata 833.

def find_replace_string(s, indices, sources, targets):
    n = len(s)
    at = [-1] * n
    for k in range(len(indices)):
        i = indices[k]
        if s[i:].startswith(sources[k]):
            at[i] = k
    out = []
    i = 0
    while i < n:
        k = at[i]
        if k >= 0:
            out.append(targets[k])
            i += len(sources[k])
        else:
            out.append(s[i:i + 1])
            i += 1
    return "".join(out)

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def letter(r):
    return chr(ord("a") + r)

def random_word(length, letters):
    return "".join(letter(next_random() % letters) for _ in range(length))

def show_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"

def show(s, indices, sources, targets):
    out = find_replace_string(s, indices, sources, targets)
    print(f'"{s}" {show_list(indices)} {show_list(sources)} {show_list(targets)} -> "{out}"')

def fold(check, s):
    c = check
    for b in s.encode():
        c = (c * 31 + b) % 1000000007
    return c

def random_case(n, letters, max_ops, max_len):
    s = random_word(n, letters)
    indices = []
    sources = []
    targets = []
    pos = next_random() % 4
    while pos < n and len(indices) < max_ops:
        room = n - pos if n - pos < max_len else max_len
        length = 1 + next_random() % room
        src = s[pos:pos + length]
        if next_random() % 3 == 2:
            last = ord(src[-1]) - 97
            src = src[:length - 1] + letter((last + 1) % 26)
        indices.append(pos)
        sources.append(src)
        tlen = 1 + next_random() % 7
        targets.append(random_word(tlen, 26))
        pos += length + next_random() % 4
    k = len(indices)
    i = k
    while i > 1:
        j = next_random() % i
        i -= 1
        indices[i], indices[j] = indices[j], indices[i]
        sources[i], sources[j] = sources[j], sources[i]
        targets[i], targets[j] = targets[j], targets[i]
    return find_replace_string(s, indices, sources, targets)

def main():
    global seed
    show("abcd", [0, 2], ["a", "cd"], ["eee", "ffff"])
    show("abcd", [0, 2], ["ab", "ec"], ["eee", "ffff"])
    show("vmokgggqzp", [3, 5, 1], ["kg", "ggq", "mo"], ["s", "so", "bfr"])
    show("a", [0], ["a"], ["b"])
    show("a", [0], ["b"], ["c"])
    show("abc", [1], ["bcd"], ["x"])
    show("abc", [2, 0], ["c", "a"], ["zz", "yy"])
    show("abcdef", [0], ["abcdef"], ["q"])
    show("abc", [0, 2], ["abx", "c"], ["q", "x"])
    show("abcd", [1, 1], ["bc", "bd"], ["xy", "z"])
    seed = 833
    big = random_case(1000, 2, 100, 50)
    print(f"1000 letters, 100 operations -> {len(big)} letters, checksum {fold(0, big)}")
    total = 0
    check = 0
    for rnd in range(300):
        n = 1 + next_random() % 200
        max_len = 6 if rnd % 2 == 0 else 50
        out = random_case(n, 2 + rnd % 3, 100, max_len)
        total += len(out)
        check = fold(check, out)
    print(f"300 random cases: {total} letters, checksum {check}")

main()
