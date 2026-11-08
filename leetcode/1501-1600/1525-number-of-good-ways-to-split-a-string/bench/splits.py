# LeetCode #1525: Number of Good Ways to Split a String -- bench: the ★
# arm over 200 random strings of 1 to 100000 letters, built once and
# answered 10 times.


def num_splits(s):
    b = s.encode()
    n = len(b)
    left = [0] * n
    seen = [False] * 26
    distinct = 0
    for i in range(n):
        c = b[i] - 97
        if not seen[c]:
            seen[c] = True
            distinct += 1
        left[i] = distinct
    right = [0] * n
    seen = [False] * 26
    distinct = 0
    for i in range(n - 1, -1, -1):
        c = b[i] - 97
        if not seen[c]:
            seen[c] = True
            distinct += 1
        right[i] = distinct
    good = 0
    for i in range(1, n):
        if left[i - 1] == right[i]:
            good += 1
    return good


seed = 1525


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    strings = []
    for _ in range(200):
        n = (next_random() * 32768 + next_random()) % 100000 + 1
        letters = next_random() % 26 + 1
        strings.append("".join(chr(97 + next_random() % letters) for _ in range(n)))
    check = 0
    total = 0
    for _ in range(10):
        for s in strings:
            good = num_splits(s)
            total += good
            check = mix(check, good)
    print(f"10 passes over 200 strings of up to 100000 letters: {total} good splits, checksum {check}")


main()
