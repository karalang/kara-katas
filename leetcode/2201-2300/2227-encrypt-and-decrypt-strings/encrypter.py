# LeetCode #2227: Encrypt and Decrypt Strings -- the mirror of
# encrypter.kara: a dict from key to value, and a dict from each
# dictionary word's encryption to how many words share it.


class Encrypter:
    def __init__(self, keys, values, dictionary):
        self.table = {}
        for i in range(len(keys)):
            self.table[keys[i]] = values[i]
        self.counts = {}
        for word in dictionary:
            secret = self.encrypt(word)
            if secret != "":
                self.counts[secret] = self.counts.get(secret, 0) + 1

    def encrypt(self, word1):
        secret = ""
        for c in word1:
            if c not in self.table:
                return ""
            secret += self.table[c]
        return secret

    def decrypt(self, word2):
        return self.counts.get(word2, 0)


def replay(keys, values, dictionary, calls):
    encrypter = Encrypter(keys, values, dictionary)
    answers = []
    for encrypting, word in calls:
        if encrypting:
            answers.append(encrypter.encrypt(word))
        else:
            answers.append(str(encrypter.decrypt(word)))
    return answers


seed = 2227


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def draw_case(m, v, words, longest, count):
    keys = []
    values = []
    for i in range(m):
        keys.append(chr(97 + i))
        values.append(draw_word(2, v))
    dictionary = []
    seen = set()
    for _ in range(words):
        length = next_random() % longest + 1
        word = draw_word(length, min(m + 1, 26))
        if word not in seen:
            seen.add(word)
            dictionary.append(word)
    calls = []
    for _ in range(count):
        kind = next_random() % 4
        length = next_random() % longest + 1
        if kind == 0:
            calls.append((True, draw_word(length, m)))
        else:
            if kind == 1:
                plain = dictionary[next_random() % len(dictionary)]
            else:
                plain = draw_word(length, m)
            secret = ""
            for c in plain:
                at = ord(c) - 97
                if kind == 3 or at >= m:
                    secret += draw_word(2, v)
                else:
                    secret += values[at]
            calls.append((False, secret))
    return keys, values, dictionary, calls


def show(answers):
    print("[" + ", ".join(answers) + "]")


def main():
    show(replay(list("abcd"), ["ei", "zf", "ei", "am"],
                ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"],
                [(True, "abcd"), (False, "eizfeiam")]))
    show(replay(list("ab"), ["xy", "zw"], ["ab", "ba", "aa", "c"],
                [(True, "ab"), (False, "xyzw"), (False, "zwxy"), (False, "xyxy"), (True, "ba")]))
    show(replay(list("abc"), ["qq", "qq", "qq"], ["ab", "ba", "cc", "abc", "d", "a"],
                [(False, "qqqq"), (False, "qq"), (True, "cab"), (False, "qqqqqq")]))
    check = 0
    for c in range(2000):
        m = next_random() % 26 + 1
        keys, values, dictionary, calls = draw_case(m, c % 3 + 2, 30, 5, 20)
        for answer in replay(keys, values, dictionary, calls):
            for b in answer.encode():
                check = (check * 31 + b) % 1000000007
            check = (check * 31 + 7) % 1000000007
    print(f"2000 cases: checksum {check}")
    keys, values, dictionary, calls = draw_case(26, 3, 100, 100, 200)
    answers = replay(keys, values, dictionary, calls)
    found = 0
    letters = 0
    for i, answer in enumerate(answers):
        if calls[i][0]:
            letters += len(answer)
        else:
            found += int(answer)
    print(f"200 calls: {letters} letters encrypted, {found} words found")


main()
