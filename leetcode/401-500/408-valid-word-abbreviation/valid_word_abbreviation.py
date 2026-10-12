# LeetCode #408: Valid Word Abbreviation -- mirror of
# valid_word_abbreviation.kara (two pointers).


def valid_word_abbreviation(word, abbr):
    w = word.encode()
    a = abbr.encode()
    i = 0
    j = 0
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


seed = 408


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(word, abbr):
    print(f'"{word}", "{abbr}": {"true" if valid_word_abbreviation(word, abbr) else "false"}')


show("internationalization", "i12iz4n")
show("apple", "a2e")
show("word", "4")
show("word", "04")
show("word", "w0rd")
show("a", "2")
show("ab", "1b")
show("abc", "a1c")
show("abc", "a01")
show("hi", "hi1")
show("substitution", "s10n")
show("substitution", "sub4u4")
show("substitution", "12")
show("substitution", "s55n")
show("a", "a")
show("abcdefghijklmnopqrstuvwxyz", "a24z")
valid = 0
checksum = 0
for case in range(3000):
    n = 1 + step() % 20
    word = [97 + step() % 3 for _ in range(n)]
    abbr = []
    i = 0
    number = False
    while i < n:
        if number or step() % 2 == 0:
            abbr.append(word[i])
            i += 1
            number = False
        else:
            run = 1 + step() % (n - i)
            abbr.extend(str(run).encode())
            i += run
            number = True
    kind = step() % 4
    if kind == 1:
        at = step() % len(abbr)
        abbr[at] = 97 + step() % 3
    elif kind == 2:
        at = step() % (len(abbr) + 1)
        abbr.insert(at, 48 + step() % 3)
    elif kind == 3:
        at = step() % len(abbr)
        del abbr[at]
    if valid_word_abbreviation(bytes(word).decode(), bytes(abbr).decode()):
        valid += 1
        checksum = (checksum * 31 + case + 1) % 1000000007
print(f"3000 random abbreviations: {valid} valid, checksum {checksum}")
