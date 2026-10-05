# Benchmark workload for LeetCode #345 — Python mirror of reverse_vowels.kara.

LEN = 200000
PUNCHES = 1000
MODULUS = 1073741789

VOWELS = frozenset("aeiouAEIOU")


def reverse_vowels(cs):
    i = 0
    j = len(cs) - 1
    while i < j:
        if cs[i] not in VOWELS:
            i += 1
        elif cs[j] not in VOWELS:
            j -= 1
        else:
            cs[i], cs[j] = cs[j], cs[i]
            i += 1
            j -= 1


seed = 345


def nxt():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(k):
    if k < 26:
        return chr(97 + k)
    return chr(65 + k - 26)


def main():
    s = [letter(nxt() % 32) for _ in range(LEN)]
    sink = 0
    for _ in range(PUNCHES):
        pos = (nxt() * 32768 + nxt()) % LEN
        s[pos] = letter(nxt() % 32)
        reverse_vowels(s)
        at = (nxt() * 32768 + nxt()) % LEN
        sink = (sink * 31 + ord(s[at])) % MODULUS
    print(f"sink {sink}")


main()
