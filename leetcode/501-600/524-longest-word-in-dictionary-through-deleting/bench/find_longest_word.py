# Benchmark for #524: Python mirror of the ★ arm (check every word); see
# find_longest_word.kara.


def is_subsequence(word, s):
    w = list(word)
    i = 0
    for c in s:
        if i < len(w) and w[i] == c:
            i += 1
    return i == len(w)


def find_longest_word(s, dictionary):
    best = ""
    for word in dictionary:
        if len(word) > len(best) or (len(word) == len(best) and word < best):
            if is_subsequence(word, s):
                best = word
    return best


seed = 524


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def random_subsequence(s, keep):
    word = "".join(c for c in s if next_random() % keep == 0)
    return word if word else s[0]


def main():
    texts = []
    dictionaries = []
    for _ in range(20):
        letters = 2 + next_random() % 4
        s = random_word(1000, letters)
        dictionary = []
        for _ in range(1000):
            if next_random() % 3 == 0:
                dictionary.append(random_subsequence(s, 2 + next_random() % 30))
            else:
                dictionary.append(random_word(1 + next_random() % 1000, letters))
        texts.append(s)
        dictionaries.append(dictionary)
    total = 0
    checksum = 0
    for _ in range(20):
        for c in range(len(texts)):
            answer = find_longest_word(texts[c], dictionaries[c])
            total += len(answer)
            for b in answer.encode():
                checksum = (checksum * 31 + b) % 1000000007
    print(f"20 cases, 20 rounds: total {total}, checksum {checksum}")


main()
