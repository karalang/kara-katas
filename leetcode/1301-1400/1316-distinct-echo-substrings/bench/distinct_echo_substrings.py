# LeetCode #1316 bench, Python mirror of the Kāra bench: the ★ arm (a table
# of how far every two suffixes agree, each echo counted at the first place
# it starts) on 4 strings of 2000 letters built once; then 5 passes, each
# setting one letter of every string from the checksum so far, answering it
# and folding the count plus the pass into the checksum.


def distinct_echo_substrings(text):
    s = text.encode()
    n = len(s)
    agree = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        row, below = agree[i], agree[i + 1]
        for j in range(n - 1, i, -1):
            if s[i] == s[j]:
                row[j] = below[j + 1] + 1
    earlier = [0] * n
    for i in range(n):
        row = agree[i]
        for j in range(i + 1, n):
            if row[j] > earlier[j]:
                earlier[j] = row[j]
    count = 0
    for i in range(n):
        for h in range(1, (n - i) // 2 + 1):
            if agree[i][i + h] >= h and 2 * h > earlier[i]:
                count += 1
    return count


def main():
    n = 2000
    letters = "abcdefghijklmnopqrstuvwxyz"
    seed = 1316

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for t in range(4):
        if t == 3:
            block = [letters[next_random() % 26] for _ in range(3)]
            chars = [block[i % 3] for i in range(n)]
        else:
            k = 2 if t == 0 else 3 if t == 1 else 26
            chars = [letters[next_random() % k] for _ in range(n)]
        strings.append(chars)
    check = 0
    for p in range(5):
        for t in range(4):
            chars = strings[t]
            chars[check % n] = letters[(check // 7) % 26]
            count = distinct_echo_substrings("".join(chars))
            check = (check * 31 + count + p) % 1000000007
    print(f"5 passes over 4 strings of 2000: checksum {check}")


main()
