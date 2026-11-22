# LeetCode #2839: Check if Strings Can be Made Equal With Operations I --
# the Python mirror of the ★ arm: the even places hold the same two
# letters either way round, and so do the odd ones.


def can_be_equal(s1, s2):
    def pair(x, y, p, q):
        return (x == p and y == q) or (x == q and y == p)

    return pair(s1[0], s1[2], s2[0], s2[2]) and pair(s1[1], s1[3], s2[1], s2[3])


# ---- the harness: the same in every arm --------------------------------

seed = 2839


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(w, letters):
    return "".join(chr(97 + w // letters**i % letters) for i in range(4))


def show(b):
    return "true" if b else "false"


def main():
    print(f"{show(can_be_equal('abcd', 'cdab'))} {show(can_be_equal('abcd', 'dacb'))} {show(can_be_equal('zzzz', 'zzzz'))}")
    yes = 0
    check = 0
    for a in range(81):
        for b in range(81):
            same = can_be_equal(word(a, 3), word(b, 3))
            yes += same
            check = (check * 31 + (2 if same else 1)) % 1000000007
    print(f"6561 pairs over abc: {yes} true, checksum {check}")
    yes = 0
    check = 0
    for _ in range(20000):
        hi = next_random()
        s1 = word(hi * 32768 + next_random(), 26)
        if next_random() % 2 == 0:
            cs = list(s1)
            k = next_random() % 2
            cs[k], cs[k + 2] = cs[k + 2], cs[k]
            s2 = "".join(cs)
        else:
            hi = next_random()
            s2 = word(hi * 32768 + next_random(), 26)
        same = can_be_equal(s1, s2)
        yes += same
        check = (check * 31 + (2 if same else 1)) % 1000000007
    print(f"20000 random pairs: {yes} true, checksum {check}")


main()
