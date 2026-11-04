# LeetCode #1044: Longest Duplicate Substring -- bench, Python mirror of
# longest_dup.kara (binary search on the length, rolling hash).

BASE = 131
MODULUS = 1_000_000_007


def longest_dup_substring(s):
    data = s.encode()
    low, high = 1, len(data) - 1
    best_start, best_len = 0, 0
    while low <= high:
        length = (low + high) // 2
        start = repeated_window(data, length)
        if start is not None:
            best_start, best_len = start, length
            low = length + 1
        else:
            high = length - 1
    return s[best_start:best_start + best_len]


def repeated_window(data, length):
    n = len(data)
    lead = 1
    for _ in range(1, length):
        lead = lead * BASE % MODULUS
    h = 0
    for i in range(length):
        h = (h * BASE + data[i]) % MODULUS
    seen = {}
    found = None
    start = 0
    while True:
        starts = seen.get(h)
        earlier = False
        if starts is not None:
            for j in starts:
                if same(data, j, start, length):
                    earlier = True
                    break
        if earlier:
            if found is None or smaller(data, start, found, length):
                found = start
        else:
            seen.setdefault(h, []).append(start)
        if start + length == n:
            break
        h = (h - data[start] * lead % MODULUS + MODULUS) % MODULUS
        h = (h * BASE + data[start + length]) % MODULUS
        start += 1
    return found


def same(data, a, b, length):
    for k in range(length):
        if data[a + k] != data[b + k]:
            return False
    return True


def smaller(data, a, b, length):
    for k in range(length):
        if data[a + k] != data[b + k]:
            return data[a + k] < data[b + k]
    return False


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count, n, rounds = 12, 30000, 2
    seed = [1044]
    strings = []
    for c in range(count):
        k = [2, 4, 8, 26][c % 4]
        letters = [ord("a") + next_random(seed) % k for _ in range(n)]
        if c % 2 == 1:
            src = next_random(seed) % (n // 2)
            to = n // 2 + next_random(seed) % (n // 2 - n // 8)
            for i in range(n // 8):
                letters[to + i] = letters[src + i]
        strings.append(bytes(letters).decode())
    total = check = 0
    for _ in range(rounds):
        for s in strings:
            answer = longest_dup_substring(s)
            total += len(answer)
            check = (check * 131 + len(answer) + 1) % 1000000007
            for b in answer.encode():
                check = (check * 131 + b) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: total length {total}, checksum {check}")


main()
