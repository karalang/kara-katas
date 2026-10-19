# LeetCode 791 — Custom Sort String, counting the letters.
# Mirrors custom_sort_string.kara (the ★ arm) and its harness.


def custom_sort_string(order, s):
    count = [0] * 26
    for c in s:
        count[ord(c) - 97] += 1
    named = [False] * 26
    out = []
    for c in order:
        at = ord(c) - 97
        named[at] = True
        out.append(c * count[at])
    for c in s:
        if not named[ord(c) - 97]:
            out.append(c)
    return "".join(out)


seed = 791


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(order, s):
    print(f'order = "{order}", s = "{s}" -> "{custom_sort_string(order, s)}"')


def main():
    show("cba", "abcd")
    show("bcafg", "abcd")
    show("kqep", "pekeq")
    show("z", "zzazbz")
    show("abcdefghijklmnopqrstuvwxyz", "thequickbrownfoxjumpsoverthelazydog")
    show("zyxwvutsrqponmlkjihgfedcba", "thequickbrownfoxjumpsoverthelazydog")
    show("xy", "hello")
    letters = "abcdefghijklmnopqrstuvwxyz"
    total = 0
    check = 0
    for _ in range(300):
        pool = list(letters)
        i = 25
        while i > 0:
            j = next_random() % (i + 1)
            pool[i], pool[j] = pool[j], pool[i]
            i -= 1
        order = "".join(pool[j] for j in range(1 + next_random() % 26))
        s = "".join(letters[next_random() % 26] for _ in range(1 + next_random() % 200))
        answer = custom_sort_string(order, s)
        total += len(answer)
        for b in answer.encode():
            check = (check * 131 + b) % 1000000007
    print(f"300 random strings: {total} letters, checksum {check}")


main()
