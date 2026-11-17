# LeetCode #2227: Encrypt and Decrypt Strings -- the benchmark's Python
# mirror of encrypter.kara: a dict of values and a dict counting the
# dictionary's encryptions.


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
        secret = []
        for c in word1:
            value = self.table.get(c)
            if value is None:
                return ""
            secret.append(value)
        return "".join(secret)

    def decrypt(self, word2):
        return self.counts.get(word2, 0)


seed = 2227


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    keys = []
    values = []
    for i in range(26):
        keys.append(chr(97 + i))
        values.append(draw_word(2, 3))
    dictionary = [draw_word(100, 26) for _ in range(100)]
    words = []
    for i in range(200):
        if i % 2 == 0:
            words.append(draw_word(next_random() % 2000 + 1, 26))
        elif i % 4 == 1:
            words.append("".join(values[ord(c) - 97] for c in dictionary[next_random() % 100]))
        else:
            words.append(draw_word(200, 3))
    check = 0
    for _ in range(500):
        # punch: one dictionary word drawn again before each round
        at = next_random() % 100
        dictionary[at] = draw_word(100, 26)
        encrypter = Encrypter(keys, values, dictionary)
        for i in range(200):
            if i % 2 == 0:
                secret = encrypter.encrypt(words[i])
                check = (check * 31 + len(secret) + ord(secret[len(secret) // 2])) % 1000000007
            else:
                check = (check * 31 + encrypter.decrypt(words[i])) % 1000000007
    print(f"500 rounds of 200 calls: checksum {check}")


main()
