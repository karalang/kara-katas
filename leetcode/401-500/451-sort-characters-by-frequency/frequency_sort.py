# LeetCode #451: Sort Characters By Frequency -- mirror of
# frequency_sort.kara (count, then sort the distinct characters), with
# the same harness.


def frequency_sort(s):
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    order = sorted((-n, c) for c, n in counts.items())
    return "".join(c * -negative for negative, c in order)


# ---- test harness ---------------------------------------------------------


def valid(s, out):
    if sorted(s) != sorted(out):
        return False
    seen = set()
    last_run = 1 << 63
    i = 0
    while i < len(out):
        j = i
        while j < len(out) and out[j] == out[i]:
            j += 1
        if out[i] in seen or j - i > last_run:
            return False
        seen.add(out[i])
        last_run = j - i
        i = j
    return True


def flag(b):
    return "true" if b else "false"


def show(s):
    out = frequency_sort(s)
    print(f'"{s}" -> "{out}", valid {flag(valid(s, out))}')


seed = 451


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("tree")
    show("cccaaa")
    show("Aabb")
    show("")
    show("z")
    show("dcba")
    show("2a1b2c1")
    show("mississippi")
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    count = 300
    total = 0
    all_valid = True
    checksum = 0
    for _ in range(count):
        n = next_random() % 201
        k = [1, 3, 10, 62][next_random() % 4]
        s = ""
        for _ in range(n):
            s += alphabet[next_random() % k]
        out = frequency_sort(s)
        total += len(out)
        if not valid(s, out):
            all_valid = False
        for c in out:
            checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"{count} random strings: {total} characters, all valid {flag(all_valid)}, checksum {checksum}")


main()
