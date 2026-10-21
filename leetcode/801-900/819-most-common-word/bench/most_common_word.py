# Benchmark for #819: Most Common Word -- the ★ arm (a map of counts).
#
# Mirrors most_common_word.kara: lower every letter and turn everything
# else into a space, count each word that is not banned in a dict, and
# return the word counted most, the first alphabetically of two counted
# as often.


def most_common_word(paragraph, banned):
    cleaned = "".join(c.lower() if c.isascii() and c.isalpha() else " " for c in paragraph)
    ruled_out = set(banned)
    counts = {}
    for word in cleaned.split():
        if word not in ruled_out:
            counts[word] = counts.get(word, 0) + 1
    best, most = "", 0
    for word, n in counts.items():
        if n > most or (n == most and word < best):
            best, most = word, n
    return best


seed = 819


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    length = 1 + next_random() % 10
    return "".join(chr(ord("a") + next_random() % 26) for _ in range(length))


def main():
    count = 64
    rounds = 200000
    marks = [" ", " ", " ", ", ", ". ", "! ", "? ", "; ", "' ", ","]
    vocabulary = [random_word() for _ in range(300)]
    paragraphs = []
    banned = []
    for _ in range(count):
        paragraph = ""
        while len(paragraph) < 990:
            a = next_random() % 300
            k = a * (next_random() % 300) // 300
            word = vocabulary[k]
            if next_random() % 4 == 0:
                word = word.upper()
            paragraph += word
            paragraph += marks[next_random() % 10]
        paragraphs.append(paragraph)
        ruled_out = [vocabulary[next_random() % 30] for _ in range(50)]
        ruled_out += [random_word() for _ in range(50)]
        banned.append(ruled_out)
    total = 0
    checksum = 0
    for r in range(rounds):
        g = r % count
        answer = most_common_word(paragraphs[g], banned[g])
        total += len(answer)
        for b in answer.encode():
            checksum = (checksum * 131 + b) % 1000000007
    print(f"{rounds} rounds of {count} paragraphs: total {total}, checksum {checksum}")


main()
