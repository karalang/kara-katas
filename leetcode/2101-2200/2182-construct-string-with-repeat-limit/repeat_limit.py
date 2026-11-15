# LeetCode #2182: Construct String With Repeat Limit -- the Python mirror
# of repeat_limit.kara: the letters counted, and the largest one left
# taken up to the limit, with the next largest put between when it runs
# on.


def repeat_limited_string(s, repeat_limit):
    counts = [0] * 26
    for c in s:
        counts[ord(c) - 97] += 1
    out = []
    big = 25
    while True:
        while big >= 0 and counts[big] == 0:
            big -= 1
        if big < 0:
            break
        take = min(counts[big], repeat_limit)
        out.append(chr(97 + big) * take)
        counts[big] -= take
        if counts[big] == 0:
            continue
        small = big - 1
        while small >= 0 and counts[small] == 0:
            small -= 1
        if small < 0:
            break
        out.append(chr(97 + small))
        counts[small] -= 1
    return "".join(out)


# ---- test harness ---------------------------------------------------------

seed = 2182


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def checksum(t):
    check = 0
    for c in t:
        check = (check * 31 + ord(c)) % 1000000007
    return check


def main():
    for s, k in [("cczazcc", 3), ("aababab", 2), ("a", 1), ("zzzz", 1), ("abc", 1), ("zzzzyyyy", 2), ("bbbbba", 2)]:
        print(f"\"{s}\", {k} -> \"{repeat_limited_string(s, k)}\"")
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 30 + 1
        letters = [3, 26][rnd % 2]
        k = next_random() % 5 + 1
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        t = repeat_limited_string(s, k)
        total += len(t)
        check = (check * 31 + checksum(t) + k) % 1000000007
    print(f"2000 strings: {total} letters kept, checksum {check}")
    s = "".join(chr(97 + next_random() % 26) for _ in range(100000))
    t = repeat_limited_string(s, 1)
    print(f"100000 random letters, limit 1: {len(t)} kept, checksum {checksum(t)}")
    s = "z" * 99999 + "a"
    for k in [1, 50000, 100000]:
        t = repeat_limited_string(s, k)
        print(f"99999 z and one a, limit {k}: {len(t)} kept, checksum {checksum(t)}")


main()
