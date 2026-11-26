# LeetCode #1433: Check If a String Can Break Another String -- the Python
# mirror of check_if_can_break.kara: both strings sorted, and one at least
# the other at every place


def check_if_can_break(s1, s2):
    a = sorted(s1.encode())
    b = sorted(s2.encode())
    return all(x >= y for x, y in zip(a, b)) or all(x <= y for x, y in zip(a, b))


# ---- test harness ---------------------------------------------------------

seed = 1433


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, k):
    return "".join(chr(ord('a') + next_random() % k) for _ in range(n))


def nudged(s):
    t = []
    for c in s:
        up = next_random() % 2 if c < 'z' else 0
        t.append(chr(ord(c) + up))
    return "".join(t)


def show(b):
    return "true" if b else "false"


def main():
    pairs = [("abc", "xya"), ("abe", "acd"), ("leetcodee", "interview"), ("a", "a"),
             ("ab", "ba"), ("az", "by"), ("aaa", "zzz"), ("bxd", "cwc")]
    print(" ".join(show(check_if_can_break(a, b)) for a, b in pairs))
    one = drawn(100000, 26)
    two = drawn(100000, 26)
    up = nudged(one)
    print(f"10^5 letters: {show(check_if_can_break('a' * 100000, 'z' * 100000))} {show(check_if_can_break(one, two))} {show(check_if_can_break(up, one))}")
    check = 0
    breaks = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        k = 1 + next_random() % 26
        a = drawn(n, k)
        b = drawn(n, k) if next_random() % 2 == 0 else nudged(a)
        got = check_if_can_break(a, b)
        if got:
            breaks += 1
        check = (check * 3 + (2 if got else 1)) % 1000000007
    print(f"2000 random pairs: {breaks} can break, checksum {check}")


main()
