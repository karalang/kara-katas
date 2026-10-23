# LeetCode #917: Reverse Only Letters -- Python mirror of the two pointers
# swapping letters in reverse_only_letters.kara, with its harness.


def is_letter(b):
    return ord("a") <= b <= ord("z") or ord("A") <= b <= ord("Z")


def reverse_only_letters(s):
    data = bytearray(s.encode())
    i = 0
    j = len(data)
    while i < j:
        if not is_letter(data[i]):
            i += 1
        elif not is_letter(data[j - 1]):
            j -= 1
        else:
            data[i], data[j - 1] = data[j - 1], data[i]
            i += 1
            j -= 1
    return data.decode()


seed = 917


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}": "{reverse_only_letters(s)}"')


def random_string(length, letters):
    out = []
    for _ in range(length):
        if next_random() % 100 < letters:
            c = next_random() % 26
            if next_random() % 2 == 0:
                out.append(chr(97 + c))
            else:
                out.append(chr(65 + c))
        else:
            b = 34
            while b == 34 or b == 92:
                b = 33 + next_random() % 90
            out.append(chr(b))
    return "".join(out)


def fold(check, s):
    h = check
    for b in s.encode():
        h = (h * 31 + b) % 1000000007
    return (h * 31 + 7) % 1000000007


def main():
    for s in ["ab-cd", "a-bC-dEf-ghIj", "Test1ng-Leet=code-Q!", "7_28]", "a", "?", "z<*zj", "Ab", "[a]", "aZ09^_`{zA"]:
        show(s)
    letters = 0
    check = 0
    for c in range(500):
        length = 1 + next_random() % 100
        s = random_string(length, c % 101)
        r = reverse_only_letters(s)
        letters += sum(1 for b in r.encode() if is_letter(b))
        check = fold(check, r)
    print(f"500 strings: {letters} letters, checksum {check}")
    check = 0
    for c in range(10000):
        s = random_string(100, c % 101)
        check = fold(check, reverse_only_letters(s))
    print(f"10000 strings of 100: checksum {check}")


main()
