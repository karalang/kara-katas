# LeetCode #917: Reverse Only Letters -- bench: Python mirror of the two
# pointers swapping letters in reverse_only_letters.kara.


def is_letter(b):
    return 97 <= b <= 122 or 65 <= b <= 90


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


def random_string(letters):
    out = []
    for _ in range(100):
        if next_random() % 100 < letters:
            k = next_random() % 52
            out.append(chr(97 + k) if k < 26 else chr(65 + k - 26))
        else:
            b = 34
            while b == 34 or b == 92:
                b = 33 + next_random() % 90
            out.append(chr(b))
    return "".join(out)


def main():
    rounds = 1000
    n = 1000
    pool = [random_string(c % 101) for c in range(n)]
    check = 0
    for _ in range(rounds):
        for s in pool:
            r = reverse_only_letters(s).encode()
            check = (check * 1000003 + r[0] * 256 + r[-1]) % 1000000007
    print(f"{rounds} rounds over {n} strings of 100: checksum {check}")


main()
