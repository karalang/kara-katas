# LeetCode #2840: Check if Strings Can be Made Equal With Operations II
# -- the Python mirror of the ★ arm: counts in one table of 2 x 26, s1
# up and s2 down, all back to zero.


def check_strings(s1, s2):
    count = [0] * 52
    for i, (a, b) in enumerate(zip(s1, s2)):
        side = i % 2 * 26
        count[side + ord(a) - 97] += 1
        count[side + ord(b) - 97] -= 1
    return all(n == 0 for n in count)


# ---- the harness: the same in every arm --------------------------------

seed = 2840


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, kinds):
    return [97 + next_random() % kinds for _ in range(n)]


def shuffled(s, kinds, spoil):
    t = list(s)
    n = len(t)
    for i in range(n - 1, 1, -1):
        j = i % 2 + 2 * (next_random() % (i // 2 + 1))
        if j <= i:
            t[i], t[j] = t[j], t[i]
    if spoil:
        k = next_random() % n
        t[k] = 97 + next_random() % kinds
    return t


def show(b):
    return "true" if b else "false"


def text(b):
    return bytes(b).decode()


def main():
    print(f"{show(check_strings('abcdba', 'cabdab'))} {show(check_strings('abe', 'bea'))} {show(check_strings('a', 'a'))} {show(check_strings('a', 'b'))}")
    long = letters(100000, 26)
    back = long[::-1]
    odd = long[:99999]
    odd_back = odd[::-1]
    print(f"{show(check_strings(text(long), text(back)))} {show(check_strings(text(odd), text(odd_back)))}")
    yes = 0
    check = 0
    for c in range(3300):
        if c < 3000:
            n, kinds = next_random() % 8 + 1, 3
        else:
            n, kinds = next_random() % 2000 + 1, 26
        s1 = letters(n, kinds)
        if c % 3 == 0:
            s2 = letters(n, kinds)
        elif c % 3 == 1:
            s2 = shuffled(s1, kinds, False)
        else:
            s2 = shuffled(s1, kinds, True)
        same = check_strings(text(s1), text(s2))
        yes += same
        check = (check * 31 + (2 if same else 1)) % 1000000007
        if c == 2999:
            print(f"3000 short pairs: {yes} true, checksum {check}")
            yes = 0
            check = 0
    print(f"300 long pairs: {yes} true, checksum {check}")


main()
