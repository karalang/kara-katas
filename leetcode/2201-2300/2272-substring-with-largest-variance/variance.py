# LeetCode #2272: Substring With Largest Variance -- the Python mirror of
# the ★ arm, `variance.kara`, line for line. Its output is byte-identical.

MIN = -(2 ** 63) // 2


def largest_variance(s):
    data = s.encode()
    seen = [False] * 26
    for c in data:
        seen[c - 97] = True
    best = 0
    for a in range(97, 123):
        for b in range(97, 123):
            if a == b or not seen[a - 97] or not seen[b - 97]:
                continue
            diff = 0
            with_b = MIN
            for c in data:
                if c == a:
                    diff += 1
                    with_b += 1
                elif c == b:
                    with_b = diff - 1
                    diff = max(diff - 1, 0)
                best = max(best, with_b)
    return best


seed = 2272


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(length, k):
    return "".join(chr(97 + next_random() % k) for _ in range(length))


def main():
    for s in ["aababbb", "abcde", "ab", "aaaab", "aaabaaa", "baaaab", "abababab"]:
        print(f"{s} -> {largest_variance(s)}")
    check = 0
    for t in range(2000):
        length = next_random() % 40 + 1
        s = letters(length, [2, 3, 5, 26][t % 4])
        check = (check * 31 + largest_variance(s)) % 1000000007
    print(f"2000 strings: checksum {check}")
    rand = letters(10000, 5)
    lone = "a" * 5000 + "b" + "a" * 4999
    three = letters(10000, 3)
    answers = [largest_variance(rand), largest_variance(lone), largest_variance(three)]
    print(f"10^4 letters: [{', '.join(map(str, answers))}]")


main()
