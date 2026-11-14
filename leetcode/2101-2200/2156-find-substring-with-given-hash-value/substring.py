# LeetCode #2156: Find Substring With Given Hash Value -- the Python
# mirror of substring.kara, the ★ arm: one walk from the right rolling
# the hash, the last match met kept.


def sub_str_hash(s, power, modulo, k, hash_value):
    letters = [ord(c) - ord("a") + 1 for c in s]
    n = len(letters)
    p = power % modulo
    top = 1 % modulo
    for _ in range(k):
        top = top * p % modulo
    h = 0
    start = n - k
    for i in range(n - 1, -1, -1):
        h = (h * p + letters[i]) % modulo
        if i + k < n:
            h = (h - letters[i + k] * top % modulo + modulo) % modulo
        if i + k <= n and h == hash_value:
            start = i
    return s[start:start + k]


seed = 2156


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def window_hash(s, start, k, power, modulo):
    letters = [ord(c) - ord("a") + 1 for c in s]
    h = 0
    weight = 1 % modulo
    for j in range(k):
        h = (h + letters[start + j] * weight) % modulo
        weight = weight * power % modulo
    return h


def show(s, power, modulo, k, hash_value):
    print(f'"{s}" power {power} modulo {modulo} k {k} hash {hash_value} -> "{sub_str_hash(s, power, modulo, k, hash_value)}"')


def letters(n, alphabet):
    return "".join(chr(ord("a") + next_random() % alphabet) for _ in range(n))


def main():
    show("leetcode", 7, 20, 2, 0)
    show("fbxzaad", 31, 100, 3, 32)
    show("abc", 5, 1000, 3, 86)
    show("xyz", 3, 7, 1, 5)
    show("dcba", 1, 100, 2, 5)
    show("hello", 13, 1, 3, 0)
    show("abab", 2, 100, 2, 5)
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        s = letters(n, [3, 4, 26][rnd % 3])
        k = next_random() % n + 1
        top = [10, 1000, 1000000000][rnd % 3]
        power = next_random() * 32768 % top + 1
        modulo = next_random() * 32768 % top + 1
        start = next_random() % (n - k + 1)
        hash_value = window_hash(s, start, k, power, modulo)
        found = sub_str_hash(s, power, modulo, k, hash_value)
        for c in found:
            check = (check * 31 + ord(c)) % 1000000007
        check = (check * 31 + n) % 1000000007
    print(f"2000 strings: checksum {check}")
    s = letters(20000, 26)
    for k in [1, 100, 10000, 20000]:
        power = 1000000000 - next_random()
        modulo = 1000000000 - next_random()
        start = next_random() % (20000 - k + 1)
        hash_value = window_hash(s, start, k, power, modulo)
        found = sub_str_hash(s, power, modulo, k, hash_value)
        total = 0
        for c in found:
            total = (total * 31 + ord(c)) % 1000000007
        print(f'20000 letters, k {k}: "{found[:min(8, len(found))]}", length {len(found)}, checksum {total}')


main()
