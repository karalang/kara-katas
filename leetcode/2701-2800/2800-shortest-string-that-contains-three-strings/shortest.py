# LeetCode #2800: Shortest String That Contains Three Strings -- the
# Python mirror of the ★ arm: the six orders of the three words, each
# merged left to right at the longest overlap, the shortest result, the
# least of equal lengths.


def merge(s, t):
    if t in s:
        return s
    for k in range(min(len(s), len(t)), 0, -1):
        if s.endswith(t[:k]):
            return s + t[k:]
    return s + t


def minimum_string(a, b, c):
    words = [a, b, c]
    orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    best = ""
    for order in orders:
        s = merge(merge(words[order[0]], words[order[1]]), words[order[2]])
        if best == "" or len(s) < len(best) or (len(s) == len(best) and s < best):
            best = s
    return best


seed = 2800


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(m, k):
    letters = "abcdefghijklmnopqrstuvwxyz"
    w = ""
    for _ in range(m):
        r = next_random() % k
        w += letters[r]
    return w


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    print(minimum_string("abc", "bca", "aaa"))
    print(minimum_string("ab", "ba", "aba"))
    a = "ab" * 50
    print(len(minimum_string(a, a, a)))
    joined = minimum_string("z" * 100, "y" * 100, "x" * 100)
    print(f"{len(joined)} {joined[0:3]} {joined[297:300]}")
    chain = minimum_string("abcd" * 25, "bcda" * 25, "cdab" * 25)
    print(f"{len(chain)} {digest(chain)}")
    total = 0
    check = 0
    for _ in range(3000):
        a = word(next_random() % 4 + 1, 3)
        b = word(next_random() % 4 + 1, 3)
        c = word(next_random() % 4 + 1, 3)
        s = minimum_string(a, b, c)
        total += len(s)
        check = (check * 31 + digest(s)) % 1000000007
    print(f"3000 short triples: lengths sum to {total}, checksum {check}")
    total = 0
    check = 0
    for t in range(50):
        k = 2 if t % 2 == 0 else 26
        a = word(next_random() % 100 + 1, k)
        b = word(next_random() % 100 + 1, k)
        c = word(next_random() % 100 + 1, k)
        s = minimum_string(a, b, c)
        total += len(s)
        check = (check * 31 + digest(s)) % 1000000007
    print(f"50 long triples: lengths sum to {total}, checksum {check}")


main()
