# Benchmark for #471 -- Python mirror of the ★ arm (encode_string.kara): interval DP over the encodings, with
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


# ---- bench ------------------------------------------------------------------

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
    count = 400
    size = 150
    strings = []
    for _ in range(count):
        letters = 2 + next_random() % 2
        s = ""
        while len(s) < size:
            s += random_string(letters, 2)
        strings.append(s[:size])
    total = 0
    checksum = 0
    for i in range(count):
        e = encode(strings[i])
        total += len(e)
        checksum = (checksum * 31 + len(e)) % 1000000007
    print(f"{count} strings of {size} letters: {total} letters encoded, checksum {checksum}")


main()
