# LeetCode #1542: Find Longest Awesome Substring -- Python mirror of
# awesome.kara (the ★ arm, prefix parity masks and their first places); its
# output is byte-identical.


def longest_awesome(s):
    n = len(s)
    first = [n + 1] * 1024
    first[0] = 0
    mask = 0
    best = 0
    for i, c in enumerate(s):
        mask ^= 1 << (ord(c) - ord("0"))
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


def batch(count, most):
    check = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % most + 1
        digits = next_random() % 10 + 1
        s = "".join(chr(ord("0") + next_random() % digits) for _ in range(n))
        check = mix(check, longest_awesome(s))
    print(f"{count} strings of up to {most} digits: checksum {check}")


def main():
    examples = ["3242415", "12345678", "213123", "00", "9", "0123456789", "1122334455", "10101", "90019"]
    for s in examples:
        print(f"{s} -> {longest_awesome(s)}")
    all_ = "0123456789" * 10000
    print(f"0123456789 10000 times -> {longest_awesome(all_)}")
    print(f"the same and a 0 -> {longest_awesome(all_ + '0')}")
    batch(3000, 12)
    batch(300, 1000)
    batch(30, 100000)


main()
