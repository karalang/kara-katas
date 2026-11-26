# LeetCode #1790: Check if One String Swap Can Make Strings Equal -- the ★
# arm in Python: the positions where the strings differ, none or exactly
# two that cross.


def are_almost_equal(s1, s2):
    differ = []
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            differ.append(i)
            if len(differ) > 2:
                return False
    if len(differ) == 0:
        return True
    if len(differ) == 2:
        i, j = differ
        return s1[i] == s2[j] and s1[j] == s2[i]
    return False


seed = 1790


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, most):
    return "".join(chr(97 + next_random() % most) for _ in range(n))


def swapped(s, i, j):
    chars = list(s)
    chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def show(b):
    return "true" if b else "false"


def main():
    print(" ".join(show(are_almost_equal(a, b)) for a, b in [("bank", "kanb"), ("attack", "defend"), ("kelb", "kelb"), ("abcd", "dcba")]))
    print(" ".join(show(are_almost_equal(a, b)) for a, b in [("a", "a"), ("a", "b"), ("aa", "aa"), ("ab", "ac"), ("abc", "bca")]))
    long = random_word(100, 26)
    once = swapped(long, 0, 99)
    twice = swapped(once, 10, 60)
    print(f"the most: {show(are_almost_equal(long, long))} {show(are_almost_equal(long, once))} {show(are_almost_equal(long, twice))}")
    check = 0
    for c in range(3000):
        n = 1 + next_random() % 12
        most = 1 + next_random() % 4
        s1 = random_word(n, most)
        if c % 4 == 3:
            s2 = random_word(n, most)
        else:
            t = s1
            for _ in range(c % 4):
                i = next_random() % n
                j = next_random() % n
                t = swapped(t, i, j)
            s2 = t
        check = (check * 3 + (2 if are_almost_equal(s1, s2) else 1)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
