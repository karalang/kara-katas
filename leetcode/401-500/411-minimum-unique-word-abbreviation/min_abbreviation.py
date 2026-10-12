# LeetCode #411: Minimum Unique Word Abbreviation -- mirror of
# min_abbreviation.kara (masks over the letters).


def abbreviate(t, mask):
    out = []
    run = 0
    for i in range(len(t)):
        if (mask >> i) & 1 == 1:
            if run > 0:
                out.append(str(run))
                run = 0
            out.append(t[i])
        else:
            run += 1
    if run > 0:
        out.append(str(run))
    return "".join(out)


def mask_length(m, mask):
    length = 0
    in_run = False
    for i in range(m):
        if (mask >> i) & 1 == 1:
            length += 1
            in_run = False
        elif not in_run:
            length += 1
            in_run = True
    return length


def min_abbreviation(target, dictionary):
    m = len(target)
    diffs = []
    for w in dictionary:
        if len(w) == m:
            diff = 0
            for i in range(m):
                if w[i] != target[i]:
                    diff |= 1 << i
            diffs.append(diff)
    best_mask = (1 << m) - 1
    best_length = m
    for mask in range(1 << m):
        length = mask_length(m, mask)
        if length < best_length:
            if all(mask & d != 0 for d in diffs):
                best_length = length
                best_mask = mask
    return abbreviate(target, best_mask)


seed = 411


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def abbreviates(abbr, word):
    w = word.encode()
    a = abbr.encode()
    i = j = 0
    while i < len(w) and j < len(a):
        if 48 <= a[j] <= 57:
            if a[j] == 48:
                return False
            skip = 0
            while j < len(a) and 48 <= a[j] <= 57:
                skip = skip * 10 + a[j] - 48
                j += 1
            i += skip
        else:
            if w[i] != a[j]:
                return False
            i += 1
            j += 1
    return i == len(w) and j == len(a)


def abbr_length(abbr):
    length = 0
    for j, c in enumerate(abbr):
        if not c.isdigit() or j == 0 or not abbr[j - 1].isdigit():
            length += 1
    return length


def verdict(target, dictionary, abbr):
    ok = abbreviates(abbr, target) and not any(abbreviates(abbr, d) for d in dictionary)
    return f"length {abbr_length(abbr)}, {'unique' if ok else 'NOT UNIQUE'}"


def show(target, dictionary):
    abbr = min_abbreviation(target, dictionary)
    print(f"{target} [{', '.join(dictionary)}]: {verdict(target, dictionary, abbr)}")


show("apple", ["blade"])
show("apple", ["plain", "amber", "blade"])
show("apple", [])
show("apple", ["pear", "fig", "banana"])
show("a", ["b"])
show("ab", ["aa", "bb"])
show("abcd", ["abce", "abed", "aecd", "ebcd"])
show("internationalization", ["internationalizatiom"])
show("aaaaaaaa", ["aaaaaaab", "baaaaaaa", "aaaabaaa"])
unique = 0
total = 0
checksum = 0
for _ in range(1000):
    m = 1 + step() % 8
    target = "".join(chr(97 + step() % 2) for _ in range(m))
    dictionary = []
    count = step() % 11
    for _ in range(count):
        n = 1 + step() % 8 if step() % 4 == 0 else m
        word = "".join(chr(97 + step() % 2) for _ in range(n))
        if word != target:
            dictionary.append(word)
    abbr = min_abbreviation(target, dictionary)
    length = abbr_length(abbr)
    if verdict(target, dictionary, abbr).endswith(", unique"):
        unique += 1
    total += length
    checksum = (checksum * 31 + length) % 1000000007
print(f"1000 random targets: {unique} unique, total length {total}, checksum {checksum}")
