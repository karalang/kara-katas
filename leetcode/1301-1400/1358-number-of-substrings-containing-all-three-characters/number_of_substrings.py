# LeetCode #1358 -- Python mirror of the ★ arm: where each of a, b and c
# was last seen; a substring ending at i holds all three when it starts at
# or before the earliest of those places.


def number_of_substrings(s):
    last = [-1, -1, -1]
    count = 0
    for i, ch in enumerate(s):
        last[ord(ch) - 97] = i
        count += min(last) + 1
    return count


seed = [1358]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_text(n, wa, wb, wc):
    out = []
    for _ in range(n):
        r = next_random() % (wa + wb + wc)
        out.append("a" if r < wa else "b" if r < wa + wb else "c")
    return "".join(out)


def main():
    e1 = number_of_substrings("abcabc")
    e2 = number_of_substrings("aaacb")
    e3 = number_of_substrings("abc")
    missing = number_of_substrings("ababab")
    repeated = number_of_substrings("abc" * 16666 + "ab")
    late = number_of_substrings("a" * 49998 + "bc")
    random = number_of_substrings(random_text(50000, 1, 1, 1))
    print(f"{e1} {e2} {e3} {missing} {repeated} {late} {random}")
    total = 0
    check = 0
    for c in range(2000):
        n = 3 + next_random() % 298 if c % 10 == 0 else 3 + next_random() % 15
        rare = 1 if c % 3 == 0 else 10
        got = number_of_substrings(random_text(n, 10, 10, rare))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random strings: {total} substrings in all, checksum {check}")


main()
