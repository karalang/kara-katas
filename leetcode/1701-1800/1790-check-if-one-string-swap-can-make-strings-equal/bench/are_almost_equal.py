# LeetCode #1790: Check if One String Swap Can Make Strings Equal -- the
# bench in Python, mirroring are_almost_equal.kara: the positions where the
# strings differ.


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


def main():
    pairs = []
    for k in range(2000):
        a = [97 + next_random() % 26 for _ in range(100)]
        b = list(a)
        for _ in range(k % 4):
            i = next_random() % 100
            j = next_random() % 100
            if k % 4 == 3:
                b[i] = 97 + (b[i] - 97 + 1) % 26
            else:
                b[i], b[j] = b[j], b[i]
        pairs.append((bytes(a).decode(), bytes(b).decode()))
    check = 0
    for call in range(4000000):
        s1, s2 = pairs[(check + call) % 2000]
        check = (check * 3 + (2 if are_almost_equal(s1, s2) else 1)) % 1000000007
    print(f"4000000 calls over 2000 pairs: checksum {check}")


main()
