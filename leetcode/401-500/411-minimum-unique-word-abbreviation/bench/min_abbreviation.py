# Benchmark for #411: mirror of min_abbreviation.kara (masks over the
# letters).
import sys


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
            unique = True
            for d in diffs:
                if mask & d == 0:
                    unique = False
                    break
            if unique:
                best_length = length
                best_mask = mask
    return abbreviate(target, best_mask)


seed = 411


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    targets = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    m = 20
    words = 2
    total = 0
    checksum = 0
    for _ in range(targets):
        target = "".join(chr(97 + step() % 2) for _ in range(m))
        dictionary = []
        while len(dictionary) < words:
            word = "".join(chr(97 + step() % 2) for _ in range(m))
            if word != target:
                dictionary.append(word)
        abbr = min_abbreviation(target, dictionary)
        total += len(abbr)
        for b in abbr.encode():
            checksum = (checksum * 31 + b) % 1000000007
    print(f"{targets} targets of {m} letters, {words} words each: total {total}, checksum {checksum}")


main()
