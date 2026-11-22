# LeetCode #2839: Check if Strings Can be Made Equal With Operations I --
# the bench, mirrored from equal.kara: the even pair and the odd pair,
# each either way round.


def can_be_equal(s1, s2):
    def pair(x, y, p, q):
        return (x == p and y == q) or (x == q and y == p)

    return pair(s1[0], s1[2], s2[0], s2[2]) and pair(s1[1], s1[3], s2[1], s2[3])


seed = 2839


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    return [97 + next_random() % 4 for _ in range(4)]


def main():
    count, rounds = 1000000, 20
    pairs = []
    for _ in range(count):
        a = word()
        if next_random() % 2 == 0:
            b = a[:]
            b[0], b[2] = b[2], b[0]
        else:
            b = word()
        pairs.append((bytes(a).decode(), bytes(b).decode()))
    yes = 0
    check = 0
    for r in range(rounds):
        for s1, s2 in pairs:
            same = can_be_equal(s1, s2)
            yes += same
            check = (check * 31 + (2 if same else 1) + r) % 1000000007
    print(f"{count} pairs, {rounds} rounds: {yes} true, checksum {check}")


main()
