# Benchmark for #824: Goat Latin -- the ★ arm (split, growing suffix).
#
# Mirrors goat_latin.kara: the sentence split at spaces, each word keeping
# a first vowel and moving a first consonant to the end, then "ma" and a
# run of 'a's kept in a string that grows by one letter per word.


def to_goat_latin(sentence):
    answer = []
    tail = ""
    for word in sentence.split(" "):
        tail += "a"
        first = word[0]
        if first in "aeiouAEIOU":
            answer.append(word)
        else:
            answer.append(word[1:])
            answer.append(first)
        answer.append("ma")
        answer.append(tail)
        answer.append(" ")
    answer.pop()
    return "".join(answer)


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 64
    rounds = 2000000
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rng = Random(824)
    sentences = []
    for _ in range(count):
        s = ""
        while True:
            length = 1 + rng.next() % 9
            extra = length if not s else length + 1
            if len(s) + extra > 150:
                break
            if s:
                s += " "
            for _ in range(length):
                s += letters[rng.next() % 52]
        sentences.append(s)
    total = 0
    checksum = 0
    for r in range(rounds):
        answer = to_goat_latin(sentences[r % count])
        total += len(answer)
        checksum = (checksum * 131 + ord(answer[r % len(answer)])) % 1000000007
    print(f"{rounds} rounds of {count} sentences: total {total}, checksum {checksum}")


main()
