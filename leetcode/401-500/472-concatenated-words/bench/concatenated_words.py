# Benchmark for #472 -- Python mirror of the ★ arm (concatenated_words.kara):
# shortest first, each word broken against the words before it.


def breaks(word, known):
    n = len(word)
    reach = [False] * (n + 1)
    reach[0] = True
    for end in range(1, n + 1):
        for start in range(0, end):
            if reach[start] and word[start:end] in known:
                reach[end] = True
                break
    return reach[n]


def find_all_concatenated_words_in_a_dict(words):
    order = sorted(words, key=len)
    known = set()
    found = []
    for word in order:
        if known and breaks(word, known):
            found.append(word)
        known.add(word)
    return found


# ---- bench ------------------------------------------------------------------

seed = 472


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 10000
    seen = set()
    words = []
    while len(words) < size:
        if len(words) < 1000:
            letters = 2 + next_random() % 4
            w = "".join(chr(97 + next_random() % 4) for _ in range(letters))
        else:
            parts = 2 + next_random() % 2
            w = ""
            for _ in range(parts):
                w += words[next_random() % len(words)]
            if next_random() % 4 == 0:
                w += "e"
        if len(w) <= 30 and w not in seen:
            seen.add(w)
            words.append(w)
    rounds = 10
    found = 0
    hash_sum = 0
    for _ in range(rounds):
        got = find_all_concatenated_words_in_a_dict(words)
        found += len(got)
        for w in got:
            h = 0
            for b in w.encode():
                h = (h * 31 + b) % 1000000007
            hash_sum = (hash_sum + h) % 1000000007
    print(f"{rounds} rounds on {size} words: {found} concatenated, hash sum {hash_sum}")


main()
