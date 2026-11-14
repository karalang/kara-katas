# LeetCode #1540: Can Convert String in K Moves -- Python mirror of
# convert.kara (the ★ arm, the places counted by shift); its output is
# byte-identical.


def can_convert_string(s, t, k):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[(ord(b) - ord(a) + 26) % 26] += 1
    for d in range(1, 26):
        if count[d] > 0 and d + 26 * (count[d] - 1) > k:
            return False
    return True


seed = 1540


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def batch(count, most, letters, top):
    check = 0
    yes = 0
    for _ in range(count):
        n = next_random() % most + 1
        m = next_random() % most + 1 if next_random() % 10 == 0 else n
        used = next_random() % letters + 1
        s = word(n, used)
        t = word(m, used)
        r = next_random()
        k = (r * 32768 + next_random()) % (top + 1)
        answer = can_convert_string(s, t, k)
        if answer:
            yes += 1
        check = mix(check, 1 if answer else 0)
    print(f"{count} pairs of up to {most} letters, k up to {top}: {yes} true, checksum {check}")


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        ("input", "ouput", 9),
        ("abc", "bcd", 10),
        ("aab", "bbb", 27),
        ("a", "a", 0),
        ("a", "b", 0),
        ("ab", "a", 100),
        ("az", "ba", 1),
        ("az", "ba", 26),
        ("aaa", "zzz", 77),
        ("aaa", "zzz", 76),
    ]
    for s, t, k in examples:
        print(f"{s} -> {t}, k = {k}: {show(can_convert_string(s, t, k))}")
    s = "a" * 100000
    t = "b" * 100000
    print(f"100000 a -> b, k = 2599975: {show(can_convert_string(s, t, 2599975))}")
    print(f"100000 a -> b, k = 2599974: {show(can_convert_string(s, t, 2599974))}")
    batch(3000, 12, 26, 80)
    batch(300, 1000, 26, 2000)
    batch(30, 100000, 26, 1000000000)


main()
