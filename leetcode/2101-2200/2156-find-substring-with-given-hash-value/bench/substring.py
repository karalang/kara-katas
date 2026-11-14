# LeetCode #2156: Find Substring With Given Hash Value -- the benchmark's
# Python mirror of substring.kara.


def sub_str_hash(s, power, modulo, k, hash_value):
    letters = [b - 96 for b in s.encode()]
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
    letters = s.encode()
    h = 0
    weight = 1 % modulo
    for j in range(k):
        h = (h + (letters[start + j] - 96) * weight) % modulo
        weight = weight * power % modulo
    return h


def main():
    strings = [bytearray(97 + next_random() % 26 for _ in range(20000)) for _ in range(4)]
    total = 0
    check = 0
    for rnd in range(50):
        for t in range(4):
            at = next_random() % 20000
            strings[t][at] = 97 + next_random() % 26
            s = strings[t].decode()
            k = next_random() % 20000 + 1
            power = 1000000000 - next_random()
            modulo = 1000000000 - next_random()
            start = next_random() % (20000 - k + 1)
            hash_value = window_hash(s, start, k, power, modulo)
            found = sub_str_hash(s, power, modulo, k, hash_value)
            total += len(found)
            check = (check * 31 + len(found) + ord(found[0]) + ord(found[-1]) + rnd) % 1000000007
    print(f"200 solves: {total} letters in all, checksum {check}")


main()
