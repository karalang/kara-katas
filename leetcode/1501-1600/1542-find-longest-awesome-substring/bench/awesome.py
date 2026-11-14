# LeetCode #1542: Find Longest Awesome Substring -- bench: the ★ arm (prefix
# parity masks, first places in a list) over 100 strings of 1 to 100000
# digits, each over its own first 1 to 10, built once, each asked 4 times.
# Python mirror of awesome.kara.


def longest_awesome(s):
    n = len(s)
    first = [n + 1] * 1024
    first[0] = 0
    mask = 0
    best = 0
    for i, c in enumerate(s.encode()):
        mask ^= 1 << (c - 48)
        end = i + 1
        best = max(best, end - first[mask])
        for d in range(10):
            best = max(best, end - first[mask ^ (1 << d)])
        if first[mask] > n:
            first[mask] = end
    return best


seed = 1542


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    strings = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 100000 + 1
        digits = next_random() % 10 + 1
        strings.append("".join(chr(48 + next_random() % digits) for _ in range(n)))
    check = 0
    for _ in range(4):
        for s in strings:
            check = mix(check, longest_awesome(s))
    print(f"4 passes over 100 strings of up to 100000 digits: checksum {check}")


main()
