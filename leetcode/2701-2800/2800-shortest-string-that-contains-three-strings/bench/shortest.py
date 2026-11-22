# LeetCode #2800: Shortest String That Contains Three Strings -- the
# bench in Python: the ★ arm over 2000 triples of up to 100 letters from
# a and b, all drawn first, then each answered 200 times.


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


def word(m):
    return "".join("ab"[next_random() % 2] for _ in range(m))


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    count = 2000
    rounds = 200
    cases = []
    for _ in range(count):
        a = word(next_random() % 100 + 1)
        b = word(next_random() % 100 + 1)
        c = word(next_random() % 100 + 1)
        cases.append((a, b, c))
    total = 0
    check = 0
    for r in range(rounds):
        for a, b, c in cases:
            s = minimum_string(a, b, c)
            total += len(s)
            check = (check * 31 + digest(s) + r) % 1000000007
    print(f"{count} triples of up to 100, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
