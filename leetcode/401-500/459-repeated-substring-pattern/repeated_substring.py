# LeetCode #459: Repeated Substring Pattern -- Python mirror of
# repeated_substring.kara (the star arm, every proper divisor).


def repeated_substring_pattern(s):
    cs = list(s)
    n = len(cs)
    for d in range(1, n // 2 + 1):
        if n % d != 0:
            continue
        repeats = True
        for i in range(d, n):
            if cs[i] != cs[i - d]:
                repeats = False
                break
        if repeats:
            return True
    return False


def show(s):
    answer = repeated_substring_pattern(s)
    print(f"\"{s}\" -> {'true' if answer else 'false'}")


seed = 459


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("abab")
    show("aba")
    show("abcabcabcabc")
    show("a")
    show("aa")
    show("ab")
    show("aabaaba")
    show("abaababaab")
    show("abcabcabd")
    show("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzy")
    count = 300
    found = 0
    checksum = 0
    for _ in range(count):
        letters = [1, 2, 3, 26][next_random() % 4]
        s = ""
        if next_random() % 2 == 0:
            unit = ""
            size = 1 + next_random() % 10
            for _ in range(size):
                unit += chr(97 + next_random() % letters)
            copies = 1 + next_random() % 20
            s = unit * copies
            if next_random() % 3 == 0:
                k = next_random() % len(s)
                cs = list(s)
                cs[k] = chr(97 + next_random() % 26)
                s = "".join(cs)
        else:
            n = 1 + next_random() % 200
            for _ in range(n):
                s += chr(97 + next_random() % letters)
        answer = repeated_substring_pattern(s)
        if answer:
            found += 1
        checksum = (checksum * 31 + (len(s) if answer else 1)) % 1000000007
    print(f"{count} random strings: {found} repeat a substring, checksum {checksum}")


main()
