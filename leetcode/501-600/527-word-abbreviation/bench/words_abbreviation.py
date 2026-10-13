# Benchmark for #527: Python mirror of the ★ arm (grow clashing
# prefixes); see words_abbreviation.kara.


def abbreviate(word, k):
    n = len(word)
    if k >= n - 2:
        return word
    return f"{word[:k]}{n - 1 - k}{word[n - 1]}"


def words_abbreviation(words):
    n = len(words)
    prefix = [1] * n
    abbr = [abbreviate(w, 1) for w in words]
    for i in range(n):
        while True:
            clash = [j for j in range(i + 1, n) if abbr[j] == abbr[i]]
            if not clash:
                break
            clash.append(i)
            for j in clash:
                prefix[j] += 1
                abbr[j] = abbreviate(words[j], prefix[j])
    return abbr


seed = 527


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    lists = []
    for _ in range(20):
        seen = set()
        words = []
        while len(words) < 400:
            word = random_word(8 + next_random() % 9, 2)
            if word not in seen:
                seen.add(word)
                words.append(word)
        lists.append(words)
    total = 0
    checksum = 0
    for _ in range(50):
        for words in lists:
            for a in words_abbreviation(words):
                total += len(a)
                for b in a.encode():
                    checksum = (checksum * 31 + b) % 1000000007
    print(f"20 lists of 400 words, 50 rounds: {total} letters, checksum {checksum}")


main()
