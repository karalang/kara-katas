# Benchmark for #843: Guess the Word -- Python twin of the Kāra ★ arm
# (minimax over the words still possible).


class Master:
    def __init__(self, words, secret):
        self.words = list(words)
        self.secret = secret
        self.guesses = 0
        self.found = False

    def guess(self, word):
        self.guesses += 1
        if word not in self.words:
            return -1
        if word == self.secret and self.guesses <= 10:
            self.found = True
        return sum(1 for k in range(6) if word[k] == self.secret[k])


def shared(a, b):
    count = 0
    for k in range(len(a)):
        if a[k] == b[k]:
            count += 1
    return count


def find_secret_word(words, master):
    n = len(words)
    same = [[shared(words[i], words[j]) for j in range(n)] for i in range(n)]
    possible = list(range(n))
    while possible:
        best = possible[0]
        best_worst = n + 1
        for c in possible:
            groups = [0] * 7
            row = same[c]
            for o in possible:
                groups[row[o]] += 1
            worst = max(groups[:6])
            if worst < best_worst:
                best_worst = worst
                best = c
        answer = master.guess(words[best])
        if answer == 6:
            return
        possible = [o for o in possible if same[best][o] == answer]


def main():
    count, rounds = 64, 6000
    seed = 843

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lists = []
    masters = []
    for g in range(count):
        k = [4, 8, 16, 26][g % 4]
        words = []
        while len(words) < 100:
            w = "".join(chr(97 + next_random() % k) for _ in range(6))
            if w not in words:
                words.append(w)
        secret = words[next_random() % 100]
        masters.append(Master(words, secret))
        lists.append(words)
    found = 0
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        masters[g].guesses = 0
        masters[g].found = False
        find_secret_word(lists[g], masters[g])
        if masters[g].found:
            found += 1
        checksum = (checksum * 31 + masters[g].guesses) % 1000000007
    print(f"{rounds} rounds of {count} lists: {found} found, checksum {checksum}")


main()
