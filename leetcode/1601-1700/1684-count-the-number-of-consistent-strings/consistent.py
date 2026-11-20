# LeetCode #1684: Count the Number of Consistent Strings -- mirrors
# consistent.kara, the ★ arm: a table of the 26 letters.


def count_consistent(allowed, words):
    ok = [False] * 26
    for b in allowed.encode():
        ok[b - 97] = True
    count = 0
    for word in words:
        if all(ok[b - 97] for b in word.encode()):
            count += 1
    return count


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def draw_allowed(letters, seed):
    allowed = ""
    for c in ALPHABET[:letters]:
        if seed.next() % 2 == 0:
            allowed += c
    if allowed == "":
        allowed = "a"
    return allowed


def draw_word(letters, seed):
    length = seed.next() % 10 + 1
    return "".join(ALPHABET[seed.next() % letters] for _ in range(length))


def batch(count, most, letters, seed):
    total = 0
    check = 0
    for _ in range(count):
        allowed = draw_allowed(letters, seed)
        n = seed.next() % most + 1
        words = [draw_word(letters, seed) for _ in range(n)]
        answer = count_consistent(allowed, words)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} problems of up to {most} words from {letters} letters: {total} consistent, checksum {check}")


def main():
    print(count_consistent("ab", ["ad", "bd", "aaab", "baa", "badab"]))
    print(count_consistent("abc", ["a", "b", "c", "ab", "ac", "bc", "abc"]))
    print(count_consistent("cad", ["cc", "acd", "b", "ba", "bac", "bad", "ac", "d"]))
    print(count_consistent("abcdefghijklmnopqrstuvwxyz", ["leetcode", "kara", "zzz"]))
    print(count_consistent("z", ["z", "zz", "az", "zzzzzzzzzz"]))
    seed = Seed(1684)
    batch(3000, 10, 4, seed)
    batch(300, 1000, 10, seed)
    batch(10, 10000, 26, seed)


main()
