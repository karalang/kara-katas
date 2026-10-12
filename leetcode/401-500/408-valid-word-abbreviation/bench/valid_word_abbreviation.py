# Benchmark for #408: mirror of valid_word_abbreviation.kara (two
# pointers).
import sys


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


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rounds = 1000
    n = 20
    words = []
    abbrs = []
    for _ in range(count):
        word = "".join(chr(97 + step() % 2) for _ in range(n))
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
                abbr.append(str(run))
                i += run
                number = True
        words.append(word)
        abbrs.append("".join(abbr))
    valid = 0
    checksum = 0
    for r in range(rounds):
        found = 0
        for i in range(count):
            if valid_word_abbreviation(words[i], abbrs[(i + r) % count]):
                found += 1
        valid += found
        checksum = (checksum * 31 + found) % 1000000007
    print(f"{count} words, {rounds} rounds: {valid} valid, checksum {checksum}")


main()
