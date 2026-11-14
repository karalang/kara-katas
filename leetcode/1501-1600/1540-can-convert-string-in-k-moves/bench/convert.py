# LeetCode #1540: Can Convert String in K Moves -- bench: the ★ arm (the
# places counted by shift) over 100 pairs of 1 to 20000 letters, each with
# k from 0 to 40000, built once, every pair asked 50 times. Python mirror of
# convert.kara.


def can_convert_string(s, t, k):
    if len(s) != len(t):
        return False
    s, t = s.encode(), t.encode()
    count = [0] * 26
    for i in range(len(s)):
        count[(t[i] - s[i] + 26) % 26] += 1
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


def main():
    pairs = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 20000 + 1
        used = next_random() % 26 + 1
        s = word(n, used)
        t = word(n, used)
        b = next_random()
        k = (b * 32768 + next_random()) % 40001
        pairs.append((s, t, k))
    check = 0
    yes = 0
    for _ in range(50):
        for s, t, k in pairs:
            answer = can_convert_string(s, t, k)
            if answer:
                yes += 1
            check = mix(check, 1 if answer else 0)
    print(f"50 passes over 100 pairs of up to 20000 letters: {yes} true, checksum {check}")


main()
