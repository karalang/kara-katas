# LeetCode #2840: Check if Strings Can be Made Equal With Operations II
# -- the bench, mirrored from strings.kara: counts in one table of
# 2 x 26, s1 up and s2 down.

seed = 2840


def check_strings(s1, s2):
    count = [0] * 52
    for i, (a, b) in enumerate(zip(s1, s2)):
        side = i % 2 * 26
        count[side + a - 97] += 1
        count[side + b - 97] -= 1
    return all(n == 0 for n in count)


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 200, 100000, 20
    pairs = []
    for c in range(count):
        a = bytearray(97 + next_random() % 26 for _ in range(n))
        b = bytearray(a)
        for i in range(n - 1, 1, -1):
            j = i % 2 + 2 * (next_random() % (i // 2 + 1))
            if j <= i:
                b[i], b[j] = b[j], b[i]
        if c % 2 == 1:
            k = next_random() % n
            b[k] = 97 + next_random() % 26
        pairs.append((bytes(a), bytes(b)))
    yes = 0
    check = 0
    for r in range(rounds):
        for s1, s2 in pairs:
            same = check_strings(s1, s2)
            if same:
                yes += 1
            check = (check * 31 + (2 if same else 1) + r) % 1000000007
    print(f"{count} pairs of {n}, {rounds} rounds: {yes} true, checksum {check}")


main()
