# LeetCode #1160 bench: the ★ arm's counts of each letter, the same
# workload as count_characters.kara.


def count_characters(words, chars):
    have = [0] * 26
    for c in chars:
        have[ord(c) - 97] += 1
    total = 0
    for w in words:
        need = [0] * 26
        good = True
        for c in w:
            i = ord(c) - 97
            need[i] += 1
            if need[i] > have[i]:
                good = False
                break
        if good:
            total += len(w)
    return total


def main():
    passes = 1500
    s = 1160

    def rnd():
        nonlocal s
        s = (s * 1103515245 + 12345) % 2147483648
        return s // 65536

    def word(length, k):
        return ''.join(chr(97 + rnd() % k) for _ in range(length))
    problems = []
    for p in range(12):
        kind = p % 3
        chars = word(100, 4 if kind == 1 else 26)
        words = []
        for i in range(1000):
            if kind == 0:
                words.append(word(1 + rnd() % 100, 26))
            elif kind == 1:
                words.append(word(1 + rnd() % 30, 4))
            else:
                b = [c for c in chars if rnd() % 2 == 0]
                if i % 2 == 1:
                    b.append(b[rnd() % len(b)])
                words.append(''.join(b))
        problems.append((words, chars))
    check = 0
    for p in range(passes):
        for words, chars in problems:
            check = (check * 31 + count_characters(words, chars) + p) % 1000000007
    print(f"{passes} passes over 12 problems of 1000 words: checksum {check}")


main()
