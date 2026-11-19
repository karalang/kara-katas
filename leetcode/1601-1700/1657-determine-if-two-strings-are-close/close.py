# LeetCode #1657: Determine if Two Strings Are Close -- the Python mirror
# of the ★ arm: the same letters, and the same counts once sorted.


def close_strings(word1, word2):
    count1 = [0] * 26
    count2 = [0] * 26
    for c in word1:
        count1[ord(c) - ord("a")] += 1
    for c in word2:
        count2[ord(c) - ord("a")] += 1
    for i in range(26):
        if (count1[i] == 0) != (count2[i] == 0):
            return False
    return sorted(count1) == sorted(count2)


# ---- the harness: the same as every arm's ---------------------------------

seed = 1657


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def batch(count, most, letters):
    check = 0
    close = 0
    for _ in range(count):
        n = next_random() % most + 1
        alphabet = next_random() % letters + 1
        word1 = random_word(n, alphabet)
        if next_random() % 2 == 0:
            word2 = random_word(next_random() % most + 1, alphabet)
        else:
            cs = list(word1)
            for i in range(len(cs) - 1, 0, -1):
                j = next_random() % (i + 1)
                cs[i], cs[j] = cs[j], cs[i]
            a = chr(ord("a") + next_random() % alphabet)
            b = chr(ord("a") + next_random() % alphabet)
            word2 = "".join(b if c == a else a if c == b else c for c in cs)
        answer = close_strings(word1, word2)
        if answer:
            close += 1
        check = (check * 31 + (2 if answer else 1)) % 1000000007
    print(f"{count} pairs of up to {most} letters from {letters}: {close} close, checksum {check}")


def show(b):
    return "true" if b else "false"


print(show(close_strings("abc", "bca")))
print(show(close_strings("a", "aa")))
print(show(close_strings("cabbba", "abbccc")))
print(show(close_strings("ab", "abb")))
print(show(close_strings("aab", "aac")))
print(show(close_strings("aabbb", "aaabb")))
batch(3000, 8, 3)
batch(1000, 1000, 26)
batch(20, 100000, 26)
