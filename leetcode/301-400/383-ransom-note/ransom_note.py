# LeetCode #383: Ransom Note -- mirror of ransom_note.kara.


def can_construct(ransom_note, magazine):
    count = [0] * 26
    for b in magazine.encode():
        count[b - 97] += 1
    for b in ransom_note.encode():
        count[b - 97] -= 1
        if count[b - 97] < 0:
            return False
    return True


def show(note, magazine):
    answer = "true" if can_construct(note, magazine) else "false"
    print(f'"{note}" from "{magazine}": {answer}')


def main():
    show("a", "b")
    show("aa", "ab")
    show("aa", "aab")
    show("", "abc")
    show("", "")
    show("a", "")
    show("abc", "cba")
    show("zzz", "zzzz")
    show("zzzz", "zzz")
    show("thequickbrownfox", "xofnworbkciuqeht")
    seed = 383
    yes = 0
    checksum = 0
    for _ in range(2000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        m = (seed // 65536) % 40
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = (seed // 65536) % 15
        magazine = []
        for _ in range(m):
            seed = (seed * 1103515245 + 12345) % 2147483648
            magazine.append(chr((seed // 65536) % 6 + 97))
        note = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            note.append(chr((seed // 65536) % 6 + 97))
        ok = can_construct("".join(note), "".join(magazine))
        if ok:
            yes += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"2000 random pairs: {yes} can be built, checksum {checksum}")


main()
