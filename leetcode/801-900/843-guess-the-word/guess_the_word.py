# LeetCode #843: Guess the Word -- Python mirror of the ★ arm and its harness.


def shared(a, b):
    return sum(1 for x, y in zip(a, b) if x == y)


def find_secret_word(words, master):
    n = len(words)
    same = [[shared(words[i], words[j]) for j in range(n)] for i in range(n)]
    possible = list(range(n))
    while possible:
        best = possible[0]
        best_worst = n + 1
        for c in possible:
            groups = [0] * 7
            for o in possible:
                groups[same[c][o]] += 1
            worst = max(groups[:6])
            if worst < best_worst:
                best_worst = worst
                best = c
        answer = master.guess(words[best])
        if answer == 6:
            return
        possible = [o for o in possible if same[best][o] == answer]


class Master:
    def __init__(self, words, secret, allowed):
        self.words = list(words)
        self.secret = secret
        self.allowed = allowed
        self.guesses = 0
        self.strays = 0
        self.found = False

    def guess(self, word):
        self.guesses += 1
        if word not in self.words:
            self.strays += 1
            return -1
        if word == self.secret and self.guesses <= self.allowed:
            self.found = True
        return shared(word, self.secret)


def verdict(words, secret, allowed):
    master = Master(words, secret, allowed)
    find_secret_word(words, master)
    if master.found:
        return "You guessed the secret word correctly."
    return "Either you took too many guesses, or you did not find the secret word."


seed = 843


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(n, k):
    words = []
    while len(words) < n:
        w = "".join(chr(97 + next_random() % k) for _ in range(6))
        if w not in words:
            words.append(w)
    return words


def main():
    print(verdict(["acckzz", "ccbazz", "eiowzz", "abcczz"], "acckzz", 10))
    print(verdict(["hamada", "khaled"], "hamada", 10))
    print(verdict(["abcdef"], "abcdef", 10))
    family = ["aaaaa" + chr(97 + c) for c in range(26)]
    print(verdict(family, "aaaaaj", 10))
    print(verdict(family, "aaaaak", 10))
    print(verdict(family, "aaaaak", 30))
    binary = ["".join("b" if (m >> k) & 1 else "a" for k in range(6)) for m in range(64)]
    print(verdict(binary, "abbaba", 10))
    print(verdict(binary, "bbbbbb", 10))
    many = random_words(100, 26)
    print(verdict(many, many[57], 10))
    close = random_words(100, 3)
    print(verdict(close, close[99], 10))
    found = 0
    check = 0
    for t in range(300):
        k = 2 + next_random() % 25
        n = min(1 + next_random() % 100, k ** 6)
        words = random_words(n, k)
        secret = words[next_random() % n]
        ok = verdict(words, secret, 10).startswith("You")
        if ok:
            found += 1
        check = (check * 31 + (t if ok else 1000)) % 1000000007
    print(f"300 random lists: {found} found, checksum {check}")


main()
