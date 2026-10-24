# LeetCode #936: Stamping The Sequence -- stamps peeled off in reverse
# (Python mirror).


def moves_to_stamp(stamp, target):
    s = stamp
    t = list(target)
    m = len(s)
    n = len(t)
    erased = 0
    order = []
    progress = True
    while progress and erased < n:
        progress = False
        for p in range(n - m + 1):
            fits = True
            fresh = False
            for k in range(m):
                if t[p + k] == s[k]:
                    fresh = True
                elif t[p + k] != "?":
                    fits = False
            if fits and fresh:
                for k in range(m):
                    if t[p + k] != "?":
                        t[p + k] = "?"
                        erased += 1
                order.append(p)
                progress = True
    if erased < n:
        return []
    order.reverse()
    return order


# ---- test harness ---------------------------------------------------------

seed = 936


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def valid(stamp, target, moves):
    m = len(stamp)
    n = len(target)
    if len(moves) > 10 * n:
        return False
    out = ["?"] * n
    for p in moves:
        if p < 0 or p > n - m:
            return False
        for k in range(m):
            out[p + k] = stamp[k]
    return "".join(out) == target


def verdict(stamp, target):
    moves = moves_to_stamp(stamp, target)
    if len(moves) == 0:
        return "cannot be stamped"
    if valid(stamp, target, moves):
        return "stamped"
    return "INVALID STAMPS"


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def stamped(stamp, n):
    m = len(stamp)
    out = ["?"] * n
    left = n
    while left > 0:
        p = next_random() % (n - m + 1)
        for k in range(m):
            if out[p + k] == "?":
                left -= 1
            out[p + k] = stamp[k]
    return "".join(out)


def main():
    cases = [
        ("abc", "ababc"),
        ("abca", "aabcaca"),
        ("abc", "abc"),
        ("a", "aaaa"),
        ("ab", "ba"),
        ("abc", "abcx"),
        ("aab", "aaaab"),
        ("abc", "aabcc"),
        ("xyz", "xyxyzyz"),
    ]
    for stamp, target in cases:
        print(f"stamp = {stamp}, target = {target}: {verdict(stamp, target)}")
    count = 0
    lengths = 0
    check = 0
    for c in range(300):
        m = 1 + next_random() % 5
        stamp = random_word(m, 3)
        n = m + next_random() % (61 - m)
        target = stamped(stamp, n)
        if c % 3 == 1:
            at = next_random() % n
            letter = chr(97 + next_random() % 3)
            target = target[:at] + letter + target[at + 1:]
        elif c % 3 == 2:
            target = random_word(n, 3)
        v = verdict(stamp, target)
        bit = 1 if v == "stamped" else 0 if v == "cannot be stamped" else 2
        if bit == 1:
            count += 1
        lengths += n
        check = (check * 31 + n * 3 + bit) % 1000000007
    print(f"300 random cases: {count} stamped, targets of {lengths} letters, checksum {check}")
    ones = "a" * 1000
    print(f"stamp a, target of 1000 a's: {verdict('a', ones)}")
    ten = random_word(10, 3)
    big = stamped(ten, 1000)
    print(f"stamp of 10 letters, target of 1000 stamped at random: {verdict(ten, big)}")
    half = random_word(500, 2)
    wide = stamped(half, 1000)
    print(f"stamp of 500 letters, target of 1000 stamped at random: {verdict(half, wide)}")
    spoiled = big[:999] + "z"
    print(f"the same target of 1000 ending in z: {verdict(ten, spoiled)}")


main()
