# LeetCode #1160: Find Words That Can Be Formed by Characters -- a Python
# mirror of the ★ arm: counts of each letter. Its output is
# byte-identical to count_characters.kara.


def count_characters(words, chars):
    have = [0] * 26
    for c in chars:
        have[ord(c) - 97] += 1
    total = 0
    for w in words:
        need = [0] * 26
        good = True
        for c in w:
            need[ord(c) - 97] += 1
            if need[ord(c) - 97] > have[ord(c) - 97]:
                good = False
                break
        if good:
            total += len(w)
    return total


# ---- test harness ---------------------------------------------------------

class Seed:
    def __init__(self, s):
        self.s = s

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s // 65536


def word(seed, length, k):
    return ''.join(chr(97 + seed.next() % k) for _ in range(length))


def show(words, chars, f):
    quoted = ', '.join(f'"{w}"' for w in words)
    print(f'[{quoted}], "{chars}" -> {f(words, chars)}')


def main(f=count_characters):
    show(["cat", "bt", "hat", "tree"], "atach", f)
    show(["hello", "world", "leetcode"], "welldonehoneyr", f)
    show(["aa", "a"], "ab", f)
    show(["abc", "cba", "abcd"], "abc", f)
    show(["z"], "a", f)
    show(["z"], "z", f)
    show(["ab", "ba", "ab"], "ab", f)
    seed = Seed(1160)
    total = check = 0
    for _ in range(2000):
        k = [1, 2, 3, 4, 5, 6, 26][seed.next() % 7]
        n = 1 + seed.next() % 20
        words = []
        for _ in range(n):
            words.append(word(seed, 1 + seed.next() % 10, k))
        chars = word(seed, 1 + seed.next() % 30, k)
        got = f(words, chars)
        total += got
        check = (check * 31 + got + 1) % 1000000007
    print(f"2000 random problems: total {total}, checksum {check}")
    for k in [26, 3, 0]:
        chars = word(seed, 100, 26 if k == 0 else k)
        words = []
        for _ in range(1000):
            words.append(chars if k == 0 else word(seed, 1 + seed.next() % 100, k))
        print(f"1000 words, chars of 100 letters: {f(words, chars)}")


if __name__ == "__main__":
    main()
