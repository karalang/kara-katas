# Benchmark workload for LeetCode #344 — Python mirror of reverse_string.kara.

LEN = 200000
PUNCHES = 4000
MODULUS = 1073741789


def reverse_string(s):
    if len(s) < 2:
        return
    i = 0
    j = len(s) - 1
    while i < j:
        t = s[i]
        s[i] = s[j]
        s[j] = t
        i += 1
        j -= 1


seed = 344


def next_():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(k):
    if k < 16:
        return chr(97 + k)
    return chr(945 + k - 16)


def main():
    s = []
    for _ in range(LEN):
        s.append(letter(next_() % 32))
    sink = 0
    for _ in range(PUNCHES):
        x = next_()
        y = next_()
        pos = (x * 32768 + y) % LEN
        s[pos] = letter(next_() % 32)
        reverse_string(s)
        u = next_()
        v = next_()
        at = (u * 32768 + v) % LEN
        sink = (sink * 31 + ord(s[at])) % MODULUS
    print(f"sink {sink}")


main()
