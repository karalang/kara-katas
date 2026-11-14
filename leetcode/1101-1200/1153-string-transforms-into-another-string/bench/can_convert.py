# LeetCode #1153 bench -- mirrors can_convert.kara: the same 64 pairs,
# the same rounds, the ★ arm's arrays.


def can_convert(str1, str2):
    if str1 == str2:
        return True
    to = [-1] * 26
    used = [False] * 26
    letters = 0
    for p, q in zip(str1, str2):
        x, y = ord(p) - 97, ord(q) - 97
        if to[x] == -1:
            to[x] = y
        elif to[x] != y:
            return False
        if not used[y]:
            used[y] = True
            letters += 1
    return letters < 26


SEED = [1153]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    rounds = 100000
    pairs = []
    for p in range(64):
        a = [97 + next_random() % 26 for _ in range(10000)]
        mp = list(range(97, 123))
        for j in range(25, 0, -1):
            k = next_random() % (j + 1)
            mp[j], mp[k] = mp[k], mp[j]
        if p % 4 < 2:
            mp[next_random() % 26] = mp[25]
        b = a[:] if p % 4 == 3 else [mp[x - 97] for x in a]
        if p % 4 == 1:
            at = next_random() % 10000
            b[at] = 97 if b[at] == 122 else b[at] + 1
        pairs.append((bytes(a).decode(), bytes(b).decode()))
    yes = 0
    check = 0
    for r in range(rounds):
        a, b = pairs[r % 64]
        ok = can_convert(a, b)
        if ok:
            yes += 1
        check = (check * 31 + (2 if ok else 1) + r % 64) % 1000000007
    print(f"{rounds} rounds over 64 pairs of 10000 letters: {yes} convertible, checksum {check}")


main()
