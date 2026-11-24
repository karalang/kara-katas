# LeetCode #1332 bench, Python mirror of the Kāra bench: the ★ arm on 1000
# strings of 1000 letters built once, then 500 passes, each setting one
# letter of one string from the checksum so far, rebuilding that string,
# and answering every string.


def remove_palindrome_sub(s):
    n = len(s)
    for i in range(n // 2):
        if s[i] != s[n - 1 - i]:
            return 2
    return 1


seed = 1332


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 1000
    n = 1000
    letters = []
    strings = []
    for t in range(count):
        row = ['a'] * n
        for i in range(n // 2):
            c = 'a' if next_random() % 2 == 0 else 'b'
            row[i] = c
            row[n - 1 - i] = c
        if t % 2 == 1:
            k = n // 2 - 1 - t % 3
            row[k] = 'b' if row[k] == 'a' else 'a'
        strings.append(''.join(row))
        letters.append(row)
    check = 0
    for p in range(500):
        t = check % count
        at = check // count % n
        c = 'a' if check // 7 % 2 == 0 else 'b'
        letters[t][at] = c
        if p % 2 == 0:
            letters[t][n - 1 - at] = c
        strings[t] = ''.join(letters[t])
        for s in strings:
            check = (check * 31 + remove_palindrome_sub(s) + p) % 1000000007
    print(f"500 passes over 1000 strings of 1000 letters: checksum {check}")


main()
